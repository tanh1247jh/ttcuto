import json
import os
import sys
import time
import re
import math
import requests
from datetime import datetime
from time import sleep

# ==================== MÀU SẮC ====================
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
trang = "\033[1;37m"
tim = "\033[1;35m"
xanh = "\033[1;36m"
dep = "\033[38;2;160;231;229m"
v = "\033[38;2;220;200;255m"
thanh = f'\033[1;35m➤ {trang}=> '


def gradient(text, start_color=(255, 0, 255), end_color=(0, 255, 255)):
    result = ""
    length = len(text)
    for i, char in enumerate(text):
        if length > 1:
            r = int(start_color[0] + (end_color[0] - start_color[0]) * i / (length - 1))
            g = int(start_color[1] + (end_color[1] - start_color[1]) * i / (length - 1))
            b = int(start_color[2] + (end_color[2] - start_color[2]) * i / (length - 1))
        else:
            r, g, b = start_color
        result += f"\033[38;2;{r};{g};{b}m{char}"
    return result + "\033[0m"


def gradient_2(text):
    def rgb(r, g, b): return f"\033[38;2;{r};{g};{b}m"
    s, m, e = (255, 87, 34), (255, 20, 147), (255, 255, 0)
    steps = len(text)
    out = ""
    for i, c in enumerate(text):
        t = i / (steps - 1 if steps > 1 else 1)
        if t < 0.5:
            k = t / 0.5
            r = int(s[0] + (m[0] - s[0]) * k)
            g = int(s[1] + (m[1] - s[1]) * k)
            b = int(s[2] + (m[2] - s[2]) * k)
        else:
            k = (t - 0.5) / 0.5
            r = int(m[0] + (e[0] - m[0]) * k)
            g = int(m[1] + (e[1] - m[1]) * k)
            b = int(m[2] + (e[2] - m[2]) * k)
        out += rgb(r, g, b) + c
    return out + "\033[0m"


def gradient_3(text):
    def rgb(r, g, b): return f"\033[38;2;{r};{g};{b}m"
    s, e = (0, 255, 0), (0, 128, 255)
    out = ""
    for i, c in enumerate(text):
        t = i / (len(text) - 1 if len(text) > 1 else 1)
        r = int(s[0] + (e[0] - s[0]) * t)
        g = int(s[1] + (e[1] - s[1]) * t)
        b = int(s[2] + (e[2] - s[2]) * t)
        out += rgb(r, g, b) + c
    return out + "\033[0m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def line(char="─", length=60, color=xanh):
    print(f"{color}{char * length}{trang}")


def banner():
    clear_screen()
    print(gradient_3("""
╔══════════════════════════════════════════════════════════════╗
║  TOOL TTC - AUTO LOGIN + CHECK XU + ĐỔI PASS + TẶNG XU       ║
║                       Version 8.0                            ║
╚══════════════════════════════════════════════════════════════╝
"""))
    print(gradient_2("""
    ┌─────────────────────────────────────────────────────┐
    │  [1] Auto: Đăng nhập + Check Xu + Đổi Pass          │
    │  [2] Đăng nhập & Check Xu tất cả tài khoản         │
    │  [3] Đổi mật khẩu 1 tài khoản                      │
    │  [4] TẶNG XU (chuyển xu qua nick khác)             │
    │  [5] Xem danh sách tài khoản đã lưu                │
    │  [6] Thêm tài khoản mới                            │
    │  [7] Xóa tài khoản                                 │
    │  [8] RESET toàn bộ dữ liệu                         │
    │  [9] Debug file JSON                                │
    │  [0] Thoát                                         │
    └─────────────────────────────────────────────────────┘
"""))


# ==================== CLASS TƯƠNG TÁC CHÉO ====================
class TuongTacCheo:
    BASE = "https://tuongtaccheo.com"

    def __init__(self, username=None, password=None, cookie_file=None):
        self.username = username
        self.password = password
        self.ss = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        }
        self.ss.headers.update(self.headers)
        self.cookie_file = cookie_file or f"cookie_{username}.json"
        self.logged_in = False

        if cookie_file and os.path.exists(cookie_file):
            if self.load_cookie():
                self.logged_in = True

    # ---------- COOKIE ----------
    def save_cookie(self):
        try:
            cookies = self.ss.cookies.get_dict()
            with open(self.cookie_file, 'w', encoding='utf-8') as f:
                json.dump(cookies, f)
        except:
            pass

    def load_cookie(self):
        try:
            with open(self.cookie_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            self.ss.cookies.update(cookies)
            return self.is_logged_in()
        except:
            return False

    # ---------- ĐĂNG NHẬP ----------
    def login(self):
        try:
            self.ss.get(f"{self.BASE}/login.php", timeout=15)

            data = {
                'username': self.username,
                'password': self.password,
                'tendangnhap': self.username,
                'matkhau': self.password,
                'submit': 'Đăng nhập',
            }

            resp = self.ss.post(
                f"{self.BASE}/login.php",
                data=data,
                timeout=15,
                allow_redirects=True
            )

            text = resp.text.lower()
            cookies = self.ss.cookies.get_dict()

            if ('home.php' in resp.url) or ('PHPSESSID' in cookies and 'đăng nhập' not in text):
                self.logged_in = True
                self.save_cookie()
                return True

            try:
                j = resp.json()
                if j.get('status') == 'success' or 'success' in str(j).lower():
                    self.logged_in = True
                    self.save_cookie()
                    return True
            except:
                pass

            return False
        except Exception as e:
            print(f"{do}❌ Lỗi login: {e}")
            return False

    def is_logged_in(self):
        try:
            r = self.ss.get(f"{self.BASE}/home.php", timeout=10, allow_redirects=False)
            if r.status_code == 200:
                return 'login' not in r.url and 'đăng nhập' not in r.text.lower()
            return False
        except:
            return False

    # ---------- THÔNG TIN ----------
    def info(self):
        try:
            r = self.ss.get(f"{self.BASE}/home.php", timeout=15)
            if 'login' in r.url:
                return {'error': 'not_logged_in'}

            text = r.text
            xu = None
            user = self.username

            patterns = [
                r'"soduchinh">([\d,\.]+)<',
                r'soduchinh["\']?\s*[:>]\s*["\']?([\d,\.]+)',
                r'Số dư[^0-9]*([\d,\.]+)',
            ]
            for p in patterns:
                m = re.search(p, text)
                if m:
                    xu = m.group(1).replace(',', '').replace('.', '')
                    break

            m = re.search(r'class="[^"]*username[^"]*"[^>]*>([^<]+)<', text)
            if m:
                user = m.group(1).strip()

            if xu is None:
                return {'error': 'cannot_parse_xu'}

            return {'status': 'success', 'user': user, 'xu': xu}
        except Exception as e:
            return {'error': str(e)}

    def get_balance(self):
        info = self.info()
        if info.get('status') == 'success':
            return int(info['xu'])
        return None

    # ---------- ĐỔI MẬT KHẨU ----------
    def change_password(self, old_password, new_password):
        URL = f"{self.BASE}/caidat/changepass.php"
        try:
            self.ss.get(f"{self.BASE}/caidat/", timeout=15)

            data = {
                'oldpass': old_password,
                'newpass': new_password,
                'renewpass': new_password,
            }

            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': self.BASE,
                'Referer': f'{self.BASE}/caidat/',
                'X-Requested-With': 'XMLHttpRequest',
            }

            resp = self.ss.post(URL, data=data, headers=headers,
                                timeout=20, allow_redirects=True)

            # Chuẩn hóa whitespace
            raw_clean = re.sub(r'\s+', ' ', resp.text.strip())

            try:
                j = resp.json()
                return {'status': 'json', 'data': j, 'raw': resp.text}
            except:
                pass

            if raw_clean == '1':
                return {'status': 'success', 'code': '1', 'raw': resp.text}
            if raw_clean.isdigit():
                return {'status': 'code', 'code': raw_clean, 'raw': resp.text}

            text_low = resp.text.lower()
            if 'thành công' in text_low or 'success' in text_low:
                return {'status': 'success', 'raw': resp.text}
            if 'mật khẩu cũ' in text_low and ('sai' in text_low or 'không đúng' in text_low):
                return {'status': 'wrong_old_password', 'raw': resp.text}

            return {'status': 'unknown', 'raw': resp.text}
        except Exception as e:
            return {'status': 'exception', 'error': str(e)}

    # ---------- TẶNG XU (FIX v8.0) ----------
    def tang_xu(self, receiver_username, amount, my_password, loai='xu'):
        """
        Tặng xu — endpoint: /caidat/tangxu.php
        Fields: usernhan, passnicktang, sluong, loai

        Response TTC (đã kiểm chứng thực tế qua DevTools):
          - '1\\n4'  = THÀNH CÔNG (1=OK, 4=loại XU)
          - '4'      = THÀNH CÔNG
          - '1'      = THÀNH CÔNG
          - '2'      = LỖI (TTC từ chối giao dịch)
          - '3'      = Nick nhận không tồn tại
        """
        URL = f"{self.BASE}/caidat/tangxu.php"
        try:
            self.ss.get(f"{self.BASE}/caidat/index.php", timeout=15)

            data = {
                'usernhan': receiver_username,
                'passnicktang': my_password,
                'sluong': amount,
                'loai': loai,
            }

            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': self.BASE,
                'Referer': f'{self.BASE}/caidat/index.php',
                'X-Requested-With': 'XMLHttpRequest',
            }

            resp = self.ss.post(URL, data=data, headers=headers,
                                timeout=20, allow_redirects=True)

            # ✅ FIX CHÍNH: chuẩn hóa whitespace (bao gồm \n, \r, \t)
            # "1\n4" → "1 4"
            # "  4  " → "4"
            raw_clean = re.sub(r'\s+', ' ', resp.text.strip())

            # Parse JSON (chỉ coi là JSON khi là dict/list; số trần như 4 là mã TTC)
            try:
                j = resp.json()
                if isinstance(j, (dict, list)):
                    return {'status': 'json', 'data': j, 'raw': resp.text}
            except:
                pass

            # Mã phản hồi thật của TTC (lấy từ JS trang /caidat)
            code_map = {
                '0': ('no_permission', 'Bạn không có quyền tặng xu/mã lực'),
                '1': ('wrong_password', 'Mật khẩu nick tặng KHÔNG ĐÚNG'),
                '2': ('user_not_found', 'Tài khoản nhận không hợp lệ'),
                '3': ('insufficient', 'Bạn không đủ xu hoặc mã lực'),
                '4': ('success', 'TẶNG THÀNH CÔNG'),
                '5': ('invalid_amount', 'Số xu/mã lực không hợp lệ'),
                '6': ('slow_down', 'Vui lòng tặng chậm lại'),
            }
            if raw_clean in code_map:
                _st, _msg = code_map[raw_clean]
                return {'status': _st, 'code': raw_clean, 'message': _msg, 'raw': resp.text}
            for _tok in raw_clean.split():
                if _tok in code_map:
                    _st, _msg = code_map[_tok]
                    return {'status': _st, 'code': _tok, 'message': _msg, 'raw': resp.text}

            # Text "thành công"
            if 'thành công' in resp.text.lower():
                return {'status': 'success', 'raw': resp.text}

            text_low = resp.text.lower()
            if 'không đủ' in text_low:
                return {'status': 'insufficient', 'raw': resp.text}
            if 'không tồn tại' in text_low:
                return {'status': 'user_not_found', 'raw': resp.text}
            if 'mật khẩu' in text_low and ('sai' in text_low or 'không đúng' in text_low):
                return {'status': 'wrong_password', 'raw': resp.text}

            return {'status': 'unknown', 'raw': resp.text}
        except Exception as e:
            return {'status': 'exception', 'error': str(e)}


# ==================== QUẢN LÝ TÀI KHOẢN ====================
class AccountManager:
    def __init__(self, file_path='ttc_accounts.json'):
        self.file_path = file_path
        self.accounts = self.load()

    def load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                    return []
            except:
                return []
        return []

    def save(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.accounts, f, ensure_ascii=False, indent=2)

    def add(self, username, password):
        for acc in self.accounts:
            if acc.get('username') == username:
                return False, "Tài khoản đã tồn tại!"

        print(f"{vang}🔄 Đang kiểm tra đăng nhập...")
        ttc = TuongTacCheo(username, password)
        if not ttc.login():
            return False, "Sai tài khoản hoặc mật khẩu!"

        info = ttc.info()
        if info.get('status') != 'success':
            return False, "Không lấy được thông tin tài khoản!"

        account = {
            'username': username,
            'password': password,
            'xu': info['xu'],
            'added_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.accounts.append(account)
        self.save()
        return True, account

    def remove(self, index):
        if 0 <= index < len(self.accounts):
            removed = self.accounts.pop(index)
            self.save()
            cf = f"cookie_{removed['username']}.json"
            if os.path.exists(cf):
                os.remove(cf)
            return True, removed
        return False, None

    def get_all(self):
        return self.accounts

    def update_balance(self, index, xu):
        if 0 <= index < len(self.accounts):
            self.accounts[index]['xu'] = xu
            self.save()

    def update_password(self, index, new_password):
        if 0 <= index < len(self.accounts):
            self.accounts[index]['password'] = new_password
            self.save()

    def clean_invalid(self):
        valid, removed = [], []
        for acc in self.accounts:
            if isinstance(acc, dict) and 'username' in acc and 'password' in acc:
                valid.append(acc)
            else:
                removed.append(acc)
        if removed:
            self.accounts = valid
            self.save()
        return removed


# ==================== CHỨC NĂNG ====================
def validate_accounts(manager):
    accounts = manager.get_all()
    return [i + 1 for i, acc in enumerate(accounts)
            if 'username' not in acc or 'password' not in acc]


def auto_login_check_pass(manager):
    removed = manager.clean_invalid()
    if removed:
        print(f"{vang}⚠️  Đã tự động xóa {len(removed)} tài khoản lỗi!")

    accounts = manager.get_all()
    if not accounts:
        print(f"{do}❌ Chưa có tài khoản nào!")
        return

    bad = validate_accounts(manager)
    if bad:
        print(f"\n{do}⚠️  Tài khoản STT {bad} thiếu username/password!")
        return

    print(f"\n{gradient_2('🔐 CẤU HÌNH ĐỔI MẬT KHẨU:')}")
    print(f"{vang}1. Đổi tất cả acc sang cùng 1 mật khẩu mới")
    print(f"{vang}2. Đổi mỗi acc 1 mật khẩu riêng")
    print(f"{vang}0. Chỉ check xu, KHÔNG đổi mật khẩu")

    mode = input(f"\n{thanh}{luc}Chọn (0/1/2): {vang}").strip()

    common_pass = None
    if mode == '1':
        common_pass = input(f"{thanh}{luc}Nhập mật khẩu MỚI (dùng chung): {vang}").strip()
        if not common_pass:
            print(f"{do}❌ Mật khẩu không được để trống!")
            return
    elif mode not in ('0', '2'):
        print(f"{do}❌ Lựa chọn không hợp lệ!")
        return

    print(f"\n{luc}🔄 Bắt đầu xử lý {len(accounts)} tài khoản...\n")
    line("─", 70, vang)

    total, ok, fail, pass_changed = 0, 0, 0, 0

    for i, acc in enumerate(accounts, 1):
        print("\n" + gradient_2("[" + str(i) + "/" + str(len(accounts)) + "] " + acc["username"]))

        ttc = TuongTacCheo(acc['username'], acc['password'],
                           cookie_file=f"cookie_{acc['username']}.json")
        info = ttc.info()

        if info.get('status') != 'success':
            print(f"  {vang}🔄 Cookie hết hạn, login lại...")
            if not ttc.login():
                print(f"  {do}❌ Không thể đăng nhập!")
                fail += 1
                time.sleep(0.5)
                continue
            info = ttc.info()

        if info.get('status') != 'success':
            print(f"  {do}❌ Không lấy được thông tin!")
            fail += 1
            time.sleep(0.5)
            continue

        xu = int(info['xu'])
        total += xu
        ok += 1
        manager.update_balance(i - 1, xu)
        print(f"  {luc}✅ Xu: {gradient_3(f'{xu:,}'.replace(',', '.'))} {trang}Xu")

        if mode in ('1', '2'):
            if mode == '1':
                new_pass = common_pass
            else:
                new_pass = input(f"  {thanh}{luc}Mật khẩu mới cho {acc['username']}: {vang}").strip()
                if not new_pass:
                    print(f"  {vang}⚠️  Bỏ qua đổi pass!")
                    continue

            print(f"  {vang}🔄 Đang đổi mật khẩu...")
            result = ttc.change_password(acc['password'], new_pass)
            status = result.get('status')

            if status == 'success':
                print(f"  {luc}✅ Đổi mật khẩu THÀNH CÔNG!")
                manager.update_password(i - 1, new_pass)
                pass_changed += 1
            elif status == 'code':
                code = result.get('code', '')
                cm = {'1': 'Thành công', '2': 'Mật khẩu cũ sai',
                      '3': 'Mật khẩu mới không khớp'}
                print(f"  {do}❌ TTC mã: {vang}{code} {do}({cm.get(code, 'Không rõ')})")
            else:
                raw = result.get('raw', result.get('error', ''))
                txt = re.sub(r'<[^>]+>', ' ', str(raw))
                txt = re.sub(r'\s+', ' ', txt).strip()
                print(f"  {do}❌ Lỗi: {trang}{txt[:150]}")

        time.sleep(0.5)

    line("─", 70, vang)
    print(f"\n{gradient_2('📊 TỔNG KẾT:')}")
    print(f"  {luc}✅ Đăng nhập OK: {vang}{ok}{trang}/{len(accounts)}")
    print(f"  {do}❌ Thất bại:    {vang}{fail}{trang}/{len(accounts)}")
    print(f"  {xanh}💰 Tổng xu:     {vang}{total:,}".replace(',', '.') + f" {trang}Xu")
    if mode in ('1', '2'):
        print(f"  {tim}🔐 Đã đổi pass: {vang}{pass_changed}{trang}/{len(accounts)}")
    line("─", 70, vang)


def auto_login_all(manager):
    removed = manager.clean_invalid()
    if removed:
        print(f"{vang}⚠️  Đã tự động xóa {len(removed)} tài khoản lỗi!")

    accounts = manager.get_all()
    if not accounts:
        print(f"{do}❌ Chưa có tài khoản nào!")
        return

    bad = validate_accounts(manager)
    if bad:
        print(f"\n{do}⚠️  Tài khoản STT {bad} thiếu username/password!")
        return

    print(f"\n{luc}🔄 Đăng nhập {len(accounts)} tài khoản...\n")
    line("─", 60, vang)

    total, ok, fail = 0, 0, 0

    for i, acc in enumerate(accounts, 1):
        print(f"{trang}[{i}/{len(accounts)}] {vang}Đang đăng nhập {acc['username']}...{trang}",
              end='\r')

        ttc = TuongTacCheo(acc['username'], acc['password'],
                           cookie_file=f"cookie_{acc['username']}.json")
        info = ttc.info()
        if info.get('status') != 'success':
            if ttc.login():
                info = ttc.info()

        if info.get('status') == 'success':
            xu = int(info['xu'])
            total += xu
            ok += 1
            manager.update_balance(i - 1, xu)
            print(f"{luc}✅ [{i:02d}] {vang}{info['user']:<25} {trang}| Xu: "
                  f"{gradient_3(f'{xu:,}'.replace(',', '.'))} {trang}Xu")
        else:
            fail += 1
            print(f"{do}❌ [{i:02d}] {vang}{acc['username']:<25} {trang}| Lỗi!")

        time.sleep(0.3)

    line("─", 60, vang)
    print(f"\n{gradient_2('📊 TỔNG KẾT:')}")
    print(f"  {luc}✅ Thành công: {vang}{ok}{trang}/{len(accounts)}")
    print(f"  {do}❌ Thất bại:  {vang}{fail}{trang}/{len(accounts)}")
    print(f"  {xanh}💰 Tổng xu:   {vang}{total:,}".replace(',', '.') + f" {trang}Xu")
    line("─", 60, vang)


def change_password_menu(manager):
    removed = manager.clean_invalid()
    if removed:
        print(f"{vang}⚠️  Đã tự động xóa {len(removed)} tài khoản lỗi!")

    accounts = manager.get_all()
    if not accounts:
        print(f"{do}❌ Chưa có tài khoản nào!")
        return

    bad = validate_accounts(manager)
    if bad:
        print(f"\n{do}⚠️  Tài khoản STT {bad} thiếu username/password!")
        return

    show_accounts(manager)

    while True:
        try:
            idx = int(input(f"\n{thanh}{luc}Chọn STT tài khoản cần đổi pass: {vang}")) - 1
            if 0 <= idx < len(accounts):
                break
            print(f"{do}❌ Số không hợp lệ!")
        except:
            print(f"{do}❌ Vui lòng nhập số!")

    acc = accounts[idx]
    print(f"\n{luc}🔄 Đang đăng nhập {acc['username']}...")

    ttc = TuongTacCheo(acc['username'], acc['password'],
                       cookie_file=f"cookie_{acc['username']}.json")
    info = ttc.info()
    if info.get('status') != 'success':
        if ttc.login():
            info = ttc.info()

    if info.get('status') != 'success':
        print(f"{do}❌ Không thể đăng nhập!")
        return

    print(f"{luc}✅ Đăng nhập OK! Xu: {vang}{int(info['xu']):,}".replace(',', '.') + " Xu")

    new_pass = input(f"\n{thanh}{luc}Nhập mật khẩu MỚI: {vang}").strip()
    if not new_pass:
        print(f"{do}❌ Không được để trống!")
        return

    confirm = input(f"{thanh}{luc}Nhập LẠI mật khẩu mới: {vang}").strip()
    if confirm != new_pass:
        print(f"{do}❌ Mật khẩu không khớp!")
        return

    print(f"\n{luc}🔄 Đang đổi mật khẩu...")
    result = ttc.change_password(acc['password'], new_pass)
    status = result.get('status')

    if status == 'success':
        print(f"{luc}✅ Đổi mật khẩu THÀNH CÔNG!")
        manager.update_password(idx, new_pass)
    elif status == 'code':
        print(f"{do}❌ TTC mã: {vang}{result.get('code')}")
    else:
        raw = result.get('raw', result.get('error', ''))
        txt = re.sub(r'<[^>]+>', ' ', str(raw))
        txt = re.sub(r'\s+', ' ', txt).strip()
        print(f"{do}❌ Lỗi: {trang}{txt[:200]}")


def tang_xu_menu(manager):
    """[4] TẶNG XU"""
    removed = manager.clean_invalid()
    if removed:
        print(f"{vang}⚠️  Đã tự động xóa {len(removed)} tài khoản lỗi!")

    accounts = manager.get_all()
    if not accounts:
        print(f"{do}❌ Chưa có tài khoản nào!")
        return

    bad = validate_accounts(manager)
    if bad:
        print(f"\n{do}⚠️  Tài khoản STT {bad} thiếu username/password!")
        return

    # Hiển thị danh sách
    print(f"\n{gradient_2('📋 DANH SÁCH TÀI KHOẢN:')}")
    line("─", 70, vang)
    print(f"{trang}{'STT':<5}{'Username':<25}{'Số Xu':<20}")
    line("─", 70, vang)
    for i, acc in enumerate(accounts, 1):
        xu_fmt = f"{int(acc.get('xu', 0)):,}".replace(',', '.')
        print(f"{vang}{i:<5}{trang}{acc['username']:<25}{luc}{xu_fmt:<20}")
    line("─", 70, vang)

    # Chọn acc gửi
    while True:
        try:
            idx = int(input(f"\n{thanh}{luc}Chọn tài khoản GỬI (STT): {vang}")) - 1
            if 0 <= idx < len(accounts):
                break
            print(f"{do}❌ Số không hợp lệ!")
        except:
            print(f"{do}❌ Vui lòng nhập số!")

    from_acc = accounts[idx]

    # Nhập username người nhận
    print(f"\n{v}💡 Chỉ cần nhập username người nhận (nick KHÁC, không phải chính mình)")
    receiver = input(f"{thanh}{luc}Username người nhận: {vang}").strip()
    if not receiver:
        print(f"{do}❌ Không được để trống!")
        return

    if receiver.lower() == from_acc['username'].lower():
        print(f"{do}❌ Không thể tặng xu cho CHÍNH MÌNH!")
        print(f"{vang}💡 Vui lòng nhập username nick KHÁC")
        return

    # Đăng nhập
    print(f"\n{luc}🔄 Đang đăng nhập {from_acc['username']}...")
    ttc = TuongTacCheo(from_acc['username'], from_acc['password'],
                       cookie_file=f"cookie_{from_acc['username']}.json")
    info = ttc.info()
    if info.get('status') != 'success':
        print(f"{vang}🔄 Cookie hết hạn, login lại...")
        if ttc.login():
            info = ttc.info()

    if info.get('status') != 'success':
        print(f"{do}❌ Không thể đăng nhập!")
        return

    xu_hien_tai = int(info['xu'])
    xu_fmt = f"{xu_hien_tai:,}".replace(',', '.')
    print(f"{luc}✅ Đăng nhập OK! Số dư: {vang}{xu_fmt} Xu")

    # Tính phí 10% (TTC trừ tổng = ceil(số_tặng * 1.1))
    toi_da = int(xu_hien_tai / 1.1)
    phi = math.ceil(toi_da * 0.1)
    toi_da_fmt = f"{toi_da:,}".replace(',', '.')
    phi_fmt = f"{phi:,}".replace(',', '.')

    print(f"\n{v}💡 Lưu ý: TTC thu phí 10% khi tặng xu")
    print(f"{v}💰 Số dư: {vang}{xu_fmt} {v}| Phí 10%: {vang}{phi_fmt}")
    print(f"{v}🎁 Tối đa có thể tặng: {gradient_3(toi_da_fmt)} {v}Xu")

    while True:
        try:
            amount = int(input(f"\n{thanh}{luc}Nhập số xu muốn tặng: {vang}"))
            if amount <= 0:
                print(f"{do}❌ Phải > 0!")
                continue
            if amount > xu_hien_tai:
                print(f"{do}❌ Vượt quá số dư ({xu_fmt} Xu)!")
                continue
            phi_gd = math.ceil(amount * 0.1)
            tong = amount + phi_gd
            if tong > xu_hien_tai:
                print(f"{do}❌ Không đủ xu trả phí 10%!")
                print(f"{vang}💡 Tặng {amount:,}".replace(',', '.') +
                      f" cần tổng {tong:,}".replace(',', '.') +
                      f" xu (bao gồm phí {phi_gd:,})".replace(',', '.'))
                print(f"{vang}💡 Tối đa có thể tặng: {toi_da_fmt} Xu")
                continue
            break
        except:
            print(f"{do}❌ Vui lòng nhập số!")

    # Nhập mật khẩu nick tặng
    print(f"\n{do}⚠️  TTC yêu cầu mật khẩu nick tặng để xác nhận!")
    print(f"{vang}💡 Nhập mật khẩu của nick ĐANG TẶNG: {luc}{from_acc['username']}")
    my_password = input(f"{thanh}{luc}Nhập MẬT KHẨU nick tặng: {vang}").strip()
    if not my_password:
        print(f"{do}❌ Không được để trống!")
        return

    # Loại
    print(f"\n{v}Loại tặng:")
    print(f"{vang}   [1] Xu")
    print(f"{vang}   [2] Mã lực sub")
    print(f"{vang}   [3] Mã lực like page")
    print(f"{vang}   [4] Mã lực cmt tiktok")
    loai_choice = input(f"{thanh}{luc}Chọn (1-4, mặc định 1): {vang}").strip()
    loai_map = {'1': 'xu', '2': 'malucsub', '3': 'maluclikepage', '4': 'maluccmttiktok'}
    loai = loai_map.get(loai_choice, 'xu')

    phi_gd = math.ceil(amount * 0.1)

    # Xác nhận
    line("─", 60, vang)
    print(f"{gradient_2('📝 XÁC NHẬN:')}")
    print(f"  {luc}Từ:       {vang}{info['user']}  (Xu: {xu_fmt})")
    print(f"  {luc}Đến:      {vang}{receiver}")
    print(f"  {luc}Số lượng: {vang}{amount:,}".replace(',', '.'))
    print(f"  {luc}Phí 10%:  {vang}{phi_gd:,}".replace(',', '.'))
    print(f"  {luc}Tổng trừ: {vang}{(amount + phi_gd):,}".replace(',', '.'))
    print(f"  {luc}Loại:     {vang}{loai.upper()}")
    line("─", 60, vang)

    if input(f"{thanh}{luc}Xác nhận? (y/n): {vang}").lower() != 'y':
        print(f"{do}❌ Đã hủy!")
        return

    # Thực hiện
    print(f"\n{luc}🔄 Đang tặng xu...")
    result = ttc.tang_xu(receiver, amount, my_password, loai)
    status = result.get('status')

    # Tự động thử lại khi TTC yêu cầu "tặng chậm lại" (mã 6)
    retry = 0
    while status == 'slow_down' and retry < 5:
        retry += 1
        wait = 3 * retry
        print(f"{vang}⏳ TTC yêu cầu chậm lại, chờ {wait}s rồi thử lại... ({retry}/5)")
        time.sleep(wait)
        result = ttc.tang_xu(receiver, amount, my_password, loai)
        status = result.get('status')

    if status == 'success':
        code = result.get('code', '4')
        print(f"{luc}✅ TẶNG XU THÀNH CÔNG! {vang}(TTC code: {code!r})")
    elif status == 'wrong_password':
        print(f"{do}❌ Mật khẩu nick tặng KHÔNG ĐÚNG! (mã 1)")
    elif status == 'user_not_found':
        print(f"{do}❌ Tài khoản nhận KHÔNG HỢP LỆ / không tồn tại! (mã 2)")
        print(f"{vang}💡 Kiểm tra lại username người nhận: {receiver}")
    elif status == 'insufficient':
        print(f"{do}❌ Bạn KHÔNG ĐỦ xu/mã lực để tặng! (mã 3)")
    elif status == 'invalid_amount':
        print(f"{do}❌ Số xu/mã lực KHÔNG HỢP LỆ! (mã 5)")
    elif status == 'slow_down':
        print(f"{do}❌ TTC yêu cầu tặng CHẬM LẠI, thử lại sau! (mã 6)")
    elif status == 'no_permission':
        print(f"{do}❌ Bạn KHÔNG CÓ QUYỀN tặng xu/mã lực! (mã 0)")
    elif status == 'json':
        print(f"{luc}📨 JSON: {vang}{result['data']}")
    else:
        raw = result.get('raw', result.get('error', ''))
        txt = re.sub(r'<[^>]+>', ' ', str(raw))
        txt = re.sub(r'\s+', ' ', txt).strip()
        print(f"{do}❌ Phản hồi: {trang}{txt[:300]}")

    # Refresh số dư
    time.sleep(1)
    new_xu = ttc.get_balance()
    if new_xu is not None:
        chenh_lech = xu_hien_tai - new_xu
        manager.update_balance(idx, new_xu)
        print(f"{luc}💰 Số dư mới: {vang}{new_xu:,}".replace(',', '.') + " Xu")
        if chenh_lech > 0:
            print(f"{luc}📉 Đã trừ: {vang}{chenh_lech:,}".replace(',', '.') + " Xu")
        elif chenh_lech == 0:
            print(f"{vang}⚠️  Số dư không đổi — kiểm tra Lịch sử tặng xu!")


def show_accounts(manager):
    accounts = manager.get_all()
    if not accounts:
        print(f"{do}❌ Chưa có tài khoản nào!")
        return

    print(f"\n{gradient_2('📋 DANH SÁCH TÀI KHOẢN:')}")
    line("─", 75, vang)
    print(f"{trang}{'STT':<5}{'Username':<25}{'Số Xu':<20}{'Ngày Thêm':<20}")
    line("─", 75, vang)

    total = 0
    for i, acc in enumerate(accounts, 1):
        xu = int(acc.get('xu', 0))
        total += xu
        print(f"{vang}{i:<5}{trang}{acc.get('username', '?'):<25}"
              f"{luc}{f'{xu:,}'.replace(',', '.'):<20}"
              f"{trang}{acc.get('added_at', 'N/A'):<20}")
    line("─", 75, vang)
    total_fmt = f"{total:,}".replace(',', '.')
    print(f"{trang}TỔNG: {luc}{len(accounts)} acc {trang}| "
          f"Tổng xu: {gradient_3(total_fmt)} {trang}Xu")
    line("─", 75, vang)


def add_account(manager):
    print(f"\n{gradient_2('➕ THÊM TÀI KHOẢN:')}")
    username = input(f"{thanh}{luc}Username: {vang}").strip()
    password = input(f"{thanh}{luc}Password: {vang}").strip()

    if not username or not password:
        print(f"{do}❌ Không được để trống!")
        return

    ok, result = manager.add(username, password)
    if ok:
        print(f"{luc}✅ Thêm thành công!")
        print(f"  {luc}Username: {vang}{result['username']}")
        print(f"  {luc}Số xu:    {vang}{int(result['xu']):,}".replace(',', '.') + " Xu")
    else:
        print(f"{do}❌ {result}")


def remove_account(manager):
    accounts = manager.get_all()
    if not accounts:
        print(f"{do}❌ Chưa có tài khoản nào!")
        return

    show_accounts(manager)
    while True:
        try:
            idx = int(input(f"\n{thanh}{luc}STT tài khoản cần xóa: {vang}")) - 1
            if 0 <= idx < len(accounts):
                if input(f"{thanh}{do}Xóa '{accounts[idx]['username']}'? (y/n): {vang}").lower() == 'y':
                    ok, removed = manager.remove(idx)
                    if ok:
                        print(f"{luc}✅ Đã xóa: {vang}{removed['username']}")
                break
            print(f"{do}❌ Số không hợp lệ!")
        except:
            print(f"{do}❌ Vui lòng nhập số!")


def reset_all_data():
    print(f"\n{do}⚠️  CẢNH BÁO: Sẽ xóa TOÀN BỘ:")
    print(f"{vang}   - File ttc_accounts.json")
    print(f"{vang}   - Tất cả file cookie_*.json")
    print(f"\n{v}📁 Thư mục hiện tại: {trang}{os.path.abspath('.')}")

    if input(f"\n{thanh}{luc}Xác nhận? (y/n): {vang}").lower() != 'y':
        print(f"{vang}⚠️  Đã hủy!")
        return

    deleted = []
    if os.path.exists('ttc_accounts.json'):
        os.remove('ttc_accounts.json')
        deleted.append('ttc_accounts.json')

    for f in os.listdir('.'):
        if f.startswith('cookie_') and f.endswith('.json'):
            try:
                os.remove(f)
                deleted.append(f)
            except:
                pass

    print(f"\n{luc}✅ Đã xóa:")
    for d in deleted:
        print(f"  {vang}- {d}")
    print(f"\n{luc}💡 Bây giờ vào menu [6] để thêm lại tài khoản!")


def debug_json():
    path = 'ttc_accounts.json'
    print(f"\n{gradient_2('🔍 DEBUG FILE JSON:')}")
    print(f"{luc}File path: {vang}{os.path.abspath(path)}")

    if not os.path.exists(path):
        print(f"{do}❌ File không tồn tại!")
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"{luc}Kích thước: {vang}{len(content)} ký tự")
    print(f"\n{trang}{content[:2000]}")


# ==================== MAIN ====================
def main():
    manager = AccountManager()

    while True:
        banner()
        try:
            choice = input(f"{thanh}{luc}Lựa chọn: {vang}").strip()
        except:
            continue

        if choice == '1':
            auto_login_check_pass(manager)
        elif choice == '2':
            auto_login_all(manager)
        elif choice == '3':
            change_password_menu(manager)
        elif choice == '4':
            tang_xu_menu(manager)
        elif choice == '5':
            show_accounts(manager)
        elif choice == '6':
            add_account(manager)
        elif choice == '7':
            remove_account(manager)
        elif choice == '8':
            reset_all_data()
            manager = AccountManager()
        elif choice == '9':
            debug_json()
        elif choice == '0':
            print(f"\n{luc}👋 Tạm biệt!")
            sys.exit(0)
        else:
            print(f"{do}❌ Lựa chọn không hợp lệ!")

        input(f"\n{thanh}{vang}Enter để tiếp tục...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{luc}👋 Đã thoát!")
    except Exception as e:
        print(f"\n{do}❌ Lỗi: {e}")