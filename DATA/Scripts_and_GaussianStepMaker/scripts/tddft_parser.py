"""
Syed Ali Abbas Abedi

"""
from __future__ import annotations

import argparse
import csv
import glob
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

EXCITED_HEADER_RE = re.compile(
    r"Excited State\s+(\d+)\s*:\s*([A-Za-z\-]+)\s+([A-Za-z]+)?\s*([0-9.]+)\s*eV\s*([0-9.]+)\s*nm\s*f\s*=\s*([0-9.]+)",
    re.IGNORECASE,
)
TRANSITION_RE = re.compile(r"^\s*(\d+)\s*->\s*(\d+)\s*([\-+]?[0-9]*\.?[0-9]+)\s*$")
OPTIM_FLAG_RE = re.compile(r"This state for optimization and/or second-order correction\.", re.IGNORECASE)
TD_TOTAL_E_RE = re.compile(r"Total Energy,\s*E\(TD-HF/TD-DFT\)\s*=\s*([\-+]?[0-9]*\.?[0-9]+)")
ROOT_RE = re.compile(r"Root\s*=\s*(\d+)", re.IGNORECASE)

def read_lines(path: Path) -> List[str]:
    with open(path, "r", errors="ignore") as f:
        return f.readlines()

def find_root(lines: List[str]) -> Optional[int]:
    for span in (lines[:400], lines):
        for ln in span:
            m = ROOT_RE.search(ln)
            if m:
                try:
                    return int(m.group(1))
                except Exception:
                    pass
    return None

def natural_key(p: Path) -> tuple:
    """Return a tuple for human sorting: split name into text and integer chunks.
    Works even if there are multiple numbers in the filename.
    """
    s = p.name.lower()
    parts = re.split(r'(\d+)', s)
    key = []
    for part in parts:
        if part.isdigit():
            key.append(int(part))
        else:
            key.append(part)
    return tuple(key)

def gather_files(patterns: List[str]) -> List[Path]:
    out: List[Path] = []
    if not patterns:
        patterns = ["."]
    for p in patterns:
        matched = glob.glob(p, recursive=True)
        if matched:
            for m in matched:
                mp = Path(m)
                if mp.is_file() and mp.suffix.lower() in [".log", ".out"]:
                    out.append(mp)
                elif mp.is_dir():
                    out.extend(list(mp.rglob("*.log")))
                    out.extend(list(mp.rglob("*.out")))
        else:
            mp = Path(p)
            if mp.is_file() and mp.suffix.lower() in [".log", ".out"]:
                out.append(mp)
            elif mp.is_dir():
                out.extend(list(mp.rglob("*.log")))
                out.extend(list(mp.rglob("*.out")))
    # de-duplicate while preserving order then sort naturally
    seen = set()
    uniq = []
    for p in out:
        if p not in seen:
            uniq.append(p)
            seen.add(p)
    uniq.sort(key=natural_key)
    return uniq

def collect_transitions_from(lines: List[str], header_idx: int) -> List[Tuple[int,int,float]]:
    trans: List[Tuple[int,int,float]] = []
    i = header_idx + 1
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith("Excited State"):
            break
        mt = TRANSITION_RE.match(ln)
        if mt:
            src = int(mt.group(1)); dst = int(mt.group(2)); coeff = float(mt.group(3))
            trans.append((src, dst, coeff))
        i += 1
    return trans

def find_td_energy_near(lines: List[str], start_idx: int, search_span: int = 30) -> Optional[float]:
    end = min(len(lines), start_idx + search_span)
    for i in range(start_idx, end):
        me = TD_TOTAL_E_RE.search(lines[i])
        if me:
            try:
                return float(me.group(1))
            except Exception:
                return None
    return None

def parse_file(path: Path, threshold: float = 0.30, topk: int = 3, debug: bool = False) -> Dict[str, object]:
    lines = read_lines(path)
    root = find_root(lines)

    headers: List[Dict[str, object]] = []
    for idx, ln in enumerate(lines):
        mh = EXCITED_HEADER_RE.search(ln)
        if mh:
            state = int(mh.group(1))
            e_eV  = float(mh.group(4))
            lam   = float(mh.group(5))
            fosc  = float(mh.group(6))
            headers.append({"idx": idx, "state": state, "e_eV": e_eV, "lam_nm": lam, "fosc": fosc})

    flagged_steps: List[Dict[str, object]] = []
    last_seen_state = None
    last_header_idx = -1
    for idx, ln in enumerate(lines):
        mh = EXCITED_HEADER_RE.search(ln)
        if mh:
            last_seen_state = int(mh.group(1))
            last_header_idx = idx
            continue
        if OPTIM_FLAG_RE.search(ln) and last_seen_state is not None:
            e_td = find_td_energy_near(lines, idx, search_span=8) or find_td_energy_near(lines, last_header_idx, 25)
            trans = collect_transitions_from(lines, last_header_idx)
            h = next((h for h in headers if h["idx"] == last_header_idx), None)
            flagged_steps.append({
                "state": last_seen_state, "idx": last_header_idx, "e_td": e_td,
                "e_eV": h["e_eV"] if h else None, "lam_nm": h["lam_nm"] if h else None,
                "fosc": h["fosc"] if h else None, "trans": trans,
            })

    chosen = None
    if flagged_steps:
        chosen = flagged_steps[-1]
    else:
        if root is not None:
            for h in reversed(headers):
                if h["state"] == root:
                    trans = collect_transitions_from(lines, h["idx"])
                    e_td  = find_td_energy_near(lines, h["idx"], 25)
                    chosen = {"state": h["state"], "idx": h["idx"], "e_td": e_td,
                              "e_eV": h["e_eV"], "lam_nm": h["lam_nm"], "fosc": h["fosc"], "trans": trans}
                    break
        if chosen is None and headers:
            h = headers[-1]
            trans = collect_transitions_from(lines, h["idx"])
            e_td  = find_td_energy_near(lines, h["idx"], 25)
            chosen = {"state": h["state"], "idx": h["idx"], "e_td": e_td,
                      "e_eV": h["e_eV"], "lam_nm": h["lam_nm"], "fosc": h["fosc"], "trans": trans}

    result: Dict[str, object] = {
        "file": str(path.name),
        "Root_in_route": root,
        "optimized_state_final": None,
        "root_matches_final": None,
        "TD_total_energy_Ha_final": None,
        "excitation_eV_final": None,
        "wavelength_nm_final": None,
        "f_osc_final": None,
        "num_transitions_final": 0,
        "adjacent_present": None,
        "adjacent_dominant": None,
        "dominant_transitions": "",
    }

    if chosen:
        st = int(chosen["state"])
        trans = chosen["trans"] or []
        result.update({
            "optimized_state_final": st,
            "root_matches_final": (root == st) if (root is not None) else None,
            "TD_total_energy_Ha_final": chosen["e_td"],
            "excitation_eV_final": chosen["e_eV"],
            "wavelength_nm_final": chosen["lam_nm"],
            "f_osc_final": chosen["fosc"],
            "num_transitions_final": len(trans),
        })
        sorted_trans = sorted(trans, key=lambda t: abs(t[2]), reverse=True)
        top = sorted_trans[:max(0, min(len(sorted_trans), topk))]
        adjacent_present  = any(abs(dst - src) == 1 and abs(coeff) >= threshold for src, dst, coeff in sorted_trans)
        adjacent_dominant = any(abs(dst - src) == 1 for src, dst, coeff in top)
        labels = []
        for src, dst, coeff in top:
            delta = dst - src
            tag = []
            if abs(delta) == 1: tag.append("adjacent")
            if abs(coeff) >= threshold: tag.append("significant")
            tag_str = (", " + ", ".join(tag)) if tag else ""
            labels.append(f"{src}->{dst} (Δ={delta}, coeff={coeff:.5f}{tag_str})")
        result["dominant_transitions"] = "; ".join(labels)
        result["adjacent_present"] = adjacent_present
        result["adjacent_dominant"] = adjacent_dominant

    if debug:
        print(f"[{Path(path).name}] Root={root}  State={result['optimized_state_final']}  "
              f"Match={result['root_matches_final']}  E_TD={result['TD_total_energy_Ha_final']}")
    return result

def run(paths: List[str], threshold: float = 0.30, top: int = 3, output: str = "td_tddft_summary.csv", debug: bool = False) -> Path:
    files = gather_files(paths)
    print(f"Found {len(files)} files.")
    if files[:5]:
        ex = [Path(f).name for f in files[:5]]
        print("Examples:", ", ".join(ex))

    rows = []
    for f in files:
        try:
            rec = parse_file(Path(f), threshold=threshold, topk=top, debug=debug)
        except Exception as e:
            rec = {"file": Path(f).name, "error": str(e)}
        rows.append(rec)

    # Natural-sort rows by 'file' to ensure CSV comes out human-ordered too
    rows.sort(key=lambda r: natural_key(Path(r.get("file",""))))

    headers = [
        "file","Root_in_route","optimized_state_final","root_matches_final",
        "TD_total_energy_Ha_final","excitation_eV_final","wavelength_nm_final",
        "f_osc_final","num_transitions_final","adjacent_present","adjacent_dominant",
        "dominant_transitions","error",
    ]
    out_path = Path(output)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in rows:
            writer.writerow({h: r.get(h) for h in headers})
    print(f"Wrote {len(rows)} rows to: {out_path.resolve()}")
    return out_path

def cli():
    ap = argparse.ArgumentParser(description="Parse Gaussian TD-DFT logs (v3, natural sort).")
    ap.add_argument("paths", nargs="*", help="Paths/globs/dirs to scan. Default: current directory.")
    ap.add_argument("--threshold", type=float, default=0.30, help="|coeff| threshold to mark a transition significant.")
    ap.add_argument("--top", type=int, default=3, help="How many top-|coeff| transitions to list.")
    ap.add_argument("--output", type=str, default="td_tddft_summary.csv", help="CSV output filename.")
    ap.add_argument("--debug", action="store_true", help="Print per-file diagnostics.")
    args = ap.parse_args()
    run(args.paths, threshold=args.threshold, top=args.top, output=args.output, debug=args.debug)

if __name__ == "__main__":
    cli()
