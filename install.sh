clear
echo "[+] Updating packages..."
pkg update -y
pkg upgrade -y

echo "[+] Installing Python..."
pkg install python -y

echo "[+] Installing pip packages..."
pip install -r requirements.txt

echo "[✓] Installation complete!"
