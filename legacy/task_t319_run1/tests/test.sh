#!/bin/bash
# PATH_COMPAT_BLOCK_BEGIN
mkdir -p /root/input /root/output
ln -sfn /root/input /input 2>/dev/null || true
ln -sfn /root/output /output 2>/dev/null || true
ln -sfn /root/input input 2>/dev/null || true
ln -sfn /root/output output 2>/dev/null || true
cp -f /root/*.pdf /root/*.csv /root/*.xlsx /root/*.json /root/*.txt /root/*.docx /root/*.m /root/*.geojson /root/*.geo.json /root/*.fastq.gz /root/*.cif /root/*.h5ad /root/*.html /root/*.xml /root/*.tsv /root/*.parquet /root/*.npy /root/*.npz /root/input/ 2>/dev/null || true
cp -f /root/* /root/input/ 2>/dev/null || true
if [ -f /root/reconcile.py ]; then
  python3 /root/reconcile.py || true
elif [ -f /solution/solve.sh ]; then
  bash /solution/solve.sh || true
fi
_expected="/root/max_avg_delay_burden_airline.json"
  _base="$(basename "$_expected")"
  _dir="$(dirname "$_expected")"
  mkdir -p "$_dir" 2>/dev/null || true
  if [ ! -e "$_expected" ] && [ -e "/root/output/$_base" ]; then cp -f "/root/output/$_base" "$_expected" 2>/dev/null || true; fi
  if [ ! -e "/root/output/$_base" ] && [ -e "/root/$_base" ]; then cp -f "/root/$_base" "/root/output/$_base" 2>/dev/null || true; fi
mkdir -p /root/output
if [ -d /root/output ]; then cp -f /root/output/* /root/ 2>/dev/null || true; fi
# PATH_COMPAT_BLOCK_END
pip3 install --break-system-packages pytest==8.4.1 pytest-json-ctrf==0.3.5
mkdir -p /logs/verifier
pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA -v
if [ $? -eq 0 ]; then echo 1 > /logs/verifier/reward.txt; else echo 0 > /logs/verifier/reward.txt; fi
exit 0
