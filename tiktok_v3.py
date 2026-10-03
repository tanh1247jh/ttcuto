import sys
import subprocess
import importlib

# (tên module để import, tên package để pip install)
REQUIRED_LIBS = [
    ("requests", "requests"),
]

def auto_install_libs():
    missing = []
    for module_name, pip_name in REQUIRED_LIBS:
        try:
            importlib.import_module(module_name)
        except ImportError:
            missing.append(pip_name)

    if not missing:
        return

    print(f"[!] Thiếu thư viện: {', '.join(missing)}")
    print("[*] Đang tự động cài đặt...")

    for pip_name in missing:
        cmds = [
            [sys.executable, "-m", "pip", "install", pip_name, "--quiet"],
            [sys.executable, "-m", "pip", "install", pip_name, "--quiet",
             "--break-system-packages"],
        ]
        for cmd in cmds:
            try:
                subprocess.check_call(cmd)
                print(f"[+] Đã cài {pip_name}")
                break
            except subprocess.CalledProcessError:
                continue
        else:
            print(f"[x] Không thể cài {pip_name}. Hãy chạy thủ công: pip install {pip_name}")
            sys.exit(1)

    print("[+] Cài đặt xong, đang khởi động tool...\n")
    importlib.invalidate_caches()

auto_install_libs()

import json
import os
import sys
import time
import random
import subprocess
import requests
from datetime import datetime
from time import sleep

# ================== GRADIENT FUNCTIONS ==================
def gradient_3(text):
    def rgb_to_ansi(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"
    start = (0, 255, 0)
    end   = (0, 128, 255)
    result = ""
    for i, char in enumerate(text):
        t = i / (len(text) - 1 if len(text) > 1 else 1)
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        result += rgb_to_ansi(r, g, b) + char
    return result + "\033[0m"

def gradient_2(text):
    def rgb_to_ansi(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"
    start_color = (255, 87, 34)
    mid_color   = (255, 20, 147)
    end_color   = (255, 255, 0)
    steps = len(text)
    result = ""
    for i, char in enumerate(text):
        t = i / (steps - 1 if steps > 1 else 1)
        if t < 0.5:
            t2 = t / 0.5
            r = int(start_color[0] + (mid_color[0] - start_color[0]) * t2)
            g = int(start_color[1] + (mid_color[1] - start_color[1]) * t2)
            b = int(start_color[2] + (mid_color[2] - start_color[2]) * t2)
        else:
            t2 = (t - 0.5) / 0.5
            r = int(mid_color[0] + (end_color[0] - mid_color[0]) * t2)
            g = int(mid_color[1] + (end_color[1] - mid_color[1]) * t2)
            b = int(mid_color[2] + (end_color[2] - mid_color[2]) * t2)
        result += rgb_to_ansi(r, g, b) + char
    return result + "\033[0m"

def gradient(text, start_color=(255, 0, 255), end_color=(0, 255, 255)):
    result = ""
    length = len(text)
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * i / max(length - 1, 1))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * i / max(length - 1, 1))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * i / max(length - 1, 1))
        result += f"\033[38;2;{r};{g};{b}m{char}"
    return result + "\033[0m"

# ================== MÀU ==================
do    = "\033[1;31m"
luc   = "\033[1;32m"
vang  = "\033[1;33m"
trang = "\033[1;37m"
tim   = "\033[1;35m"
xanh  = "\033[1;36m"
dep   = "\033[38;2;160;231;229m"
v     = "\033[38;2;220;200;255m"
thanh = f'\033[1;35m {trang}=> '

# ================== STATE ==================
list_nv = []

# ================== HIỆU ỨNG ==================
def thanhngang(so):
    for i in range(so):
        print(trang + '═', end='')
    print('')

def banner():
    print(gradient_3("""
    ╔══════════════════════════════════════════════╗
    ║        TTC TIKTOK AUTO TOOL                  ║
    ║        Get Job - Auto Follow/Like            ║
    ╚══════════════════════════════════════════════╝
    """))

def Delay(value):
    """Hiệu ứng delay Doro giống tool FB"""
    while not (value <= 1):
        value -= 0.123
        print(f'''{v}[{xanh}TTC-TT{v}] [{xanh}DELAY{v}] [{xanh}{str(value)[0:6]}{v}] [{vang}Doro   {v}]''', '           ', end='\r')
        sleep(0.02)
        print(f'''{v}[{xanh}TTC-TT{v}] [{xanh}DELAY{v}] [{xanh}{str(value)[0:6]}{v}] [ {vang}Doro   {v}]''', '           ', end='\r')
        sleep(0.02)
        print(f'''{v}[{xanh}TTC-TT{v}] [{xanh}DELAY{v}] [{xanh}{str(value)[0:6]}{v}] [  {vang}Doro {v}]''', '            ', end='\r')
        sleep(0.02)
        print(f'''{v}[{xanh}TTC-TT{v}] [{xanh}DELAY{v}] [{xanh}{str(value)[0:6]}{v}] [   {vang}Doro {v}]''', '           ', end='\r')
        sleep(0.02)
        print(f'''{v}[{xanh}TTC-TT{v}] [{xanh}DELAY{v}] [{xanh}{str(value)[0:6]}{v}] [    {vang}Doro {v}]''', '           ', end='\r')
        sleep(0.02)
    print(' ' * 70, end='\r')

# ================== MỞ LINK ==================
def is_android():
    return os.path.exists('/system/bin/pm') or 'ANDROID_ROOT' in os.environ

# Bản TikTok VN/Châu Á = trill, bản quốc tế = musically
TIKTOK_PACKAGES = ['com.ss.android.ugc.trill', 'com.zhiliaoapp.musically']
_tiktok_pkg_cache = {'done': False, 'pkg': None}

def get_tiktok_package():
    """Trả về package TikTok đang cài trên Android (None nếu chưa cài)."""
    if _tiktok_pkg_cache['done']:
        return _tiktok_pkg_cache['pkg']
    pkg = None
    try:
        r = subprocess.run(['pm', 'list', 'packages'], capture_output=True, text=True, timeout=10)
        installed = r.stdout.lower()
        for p in TIKTOK_PACKAGES:
            if p in installed:
                pkg = p
                break
    except Exception:
        pass
    _tiktok_pkg_cache.update(done=True, pkg=pkg)
    return pkg

def check_tiktok_installed_android():
    return get_tiktok_package() is not None

def open_on_android(uri, package=None):
    """Mở uri bằng intent VIEW. Có package -> ép mở thẳng trong app đó.
    Trả về True nếu lệnh am chạy thành công."""
    cmd = ['am', 'start', '-a', 'android.intent.action.VIEW', '-d', uri]
    if package:
        cmd += ['-p', package]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        out = (r.stdout or '') + (r.stderr or '')
        return r.returncode == 0 and 'Error' not in out and 'unable' not in out.lower()
    except Exception:
        return False

def open_in_tiktok_app(url, extra_uris=()):
    """Thử mở url trong app TikTok; lần lượt thử các uri phụ; cuối cùng mới mở trình duyệt."""
    pkg = get_tiktok_package()
    if pkg:
        for uri in (url, *extra_uris):
            if open_on_android(uri, pkg):
                return True
    return open_on_android(url)  # fallback: để Android tự chọn app/trình duyệt

def build_profile_url(target):
    """Nhận username / @username / link đầy đủ -> link profile chuẩn."""
    target = str(target).strip()
    if target.lower().startswith('http'):
        return target
    return f"https://www.tiktok.com/@{target.lstrip('@')}"

def open_tiktok_profile(target):
    """Mở đúng profile cần follow. target: username, @username, link, hoặc uid số."""
    target = str(target or '').strip()
    if not target:
        return False
    web_url = build_profile_url(target)
    extra = []
    # uid dạng số (không phải username) -> deep link nội bộ của app mới mở đúng người
    if target.isdigit() and len(target) >= 8:
        web_url = None
        extra = [f"snssdk1233://user/profile/{target}",
                 f"snssdk1180://user/profile/{target}"]

    if is_android():
        if web_url:
            return open_in_tiktok_app(web_url)
        pkg = get_tiktok_package()
        for uri in extra:
            if open_on_android(uri, pkg):
                return True
        print(f'{do}Không mở được profile uid {target}')
        return False

    if not web_url:
        print(f'{do}Job chỉ có uid {target}, PC không mở được profile theo uid')
        return False

    # PC: chỉ mở browser
    try:
        if os.name == 'nt':
            os.startfile(web_url)
        else:
            subprocess.Popen(['xdg-open', web_url])
        return True
    except Exception as e:
        print(f'{do}Không mở được link: {e}')
        return False

def open_tiktok_video(video_url):
    if not video_url:
        return False
    if is_android():
        return open_in_tiktok_app(video_url)
    try:
        if os.name == 'nt':
            os.startfile(video_url)
        else:
            subprocess.Popen(['xdg-open', video_url])
        return True
    except Exception as e:
        print(f'{do}Không mở được video: {e}')
        return False

# ================== TTC API ==================
class TuongTacCheo(object):
    def __init__(self, token):
        try:
            self.ss = requests.Session()
            session = self.ss.post('https://tuongtaccheo.com/logintoken.php',
                                   data={'access_token': token})
            self.cookie = session.headers['Set-cookie']
            self.session = session.json()
            self.headers = {
                'Host': 'tuongtaccheo.com',
                'accept': '*/*',
                'origin': 'https://tuongtaccheo.com',
                'x-requested-with': 'XMLHttpRequest',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                "cookie": self.cookie
            }
        except:
            self.session = {}

    def info(self):
        if self.session.get('status') == 'success':
            return {'status': "success", 'user': self.session['data']['user'],
                    'xu': self.session['data']['sodu']}
        return {'error': 200}

    def getjob(self, nv):
        try:
            return self.ss.get(f'https://tuongtaccheo.com/tiktok/kiemtien/{nv}/getpost.php',
                               headers=self.headers, timeout=15)
        except:
            return None

    def nhanxu(self, id, nv):
        try:
            xu_truoc = self.ss.get('https://tuongtaccheo.com/home.php',
                                   headers=self.headers, timeout=15).text.split('"soduchinh">')[1].split('<')[0]
            r = self.ss.post(f'https://tuongtaccheo.com/tiktok/kiemtien/{nv}/nhantien.php',
                             headers=self.headers, data={'id': id}, timeout=15).json()
            xu_sau = self.ss.get('https://tuongtaccheo.com/home.php',
                                 headers=self.headers, timeout=15).text.split('"soduchinh">')[1].split('<')[0]
            if 'mess' in r and int(xu_sau) > int(xu_truoc):
                parts = r['mess'].split()
                msg = parts[-2]
                return {'status': "success", 'msg': '+'+msg+' Xu', 'xu': xu_sau}
            return {'error': r}
        except Exception as e:
            return {'error': str(e)}

    def nhanxu_batch(self, list_job, nv):
        ok = 0
        total = 0
        xu_now = '0'
        for jid in list_job:
            r = self.nhanxu(jid, nv)
            if r.get('status') == 'success':
                ok += 1
                xu_now = r['xu']
                try:
                    total += int(r['msg'].replace(' Xu', '').replace('+', ''))
                except:
                    pass
            sleep(0.4)
        return ok, total, xu_now

# ================== MAIN ==================
os.system("cls" if os.name == "nt" else "clear")
banner()

# ---------- TOKEN TTC ----------
TOKEN_FILE = 'tokenttctiktok.json'

def load_tokens():
    """Đọc danh sách token đã lưu -> list các (token, username)."""
    if not os.path.exists(TOKEN_FILE):
        return []
    try:
        with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
            raw = json.load(f)
    except Exception:
        print(f'{do}File {TOKEN_FILE} bị lỗi, bỏ qua dữ liệu cũ.')
        return []
    accs = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, str) and '|' in item:
                tk, name = item.split('|', 1)
                if tk.strip():
                    accs.append((tk.strip(), name.strip()))
    return accs

def save_tokens(accs):
    """Lưu danh sách token (giữ định dạng cũ 'token|username')."""
    with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
        json.dump([f'{tk}|{name}' for tk, name in accs], f, ensure_ascii=False)
    try:
        os.chmod(TOKEN_FILE, 0o600)  # token là thông tin đăng nhập, hạn chế quyền đọc
    except Exception:
        pass

def login_ttc(token):
    """Thử đăng nhập token. Thành công -> (ttc, ck), thất bại -> None."""
    t = TuongTacCheo(token)
    ck = t.info()
    if ck.get('status') == 'success':
        return t, ck
    return None

def them_acc(accs):
    """Nhập token mới. Enter trống để huỷ. Trùng username thì cập nhật token."""
    while True:
        token = input(f'{thanh}{luc}Nhập Access_Token TTC (Enter để huỷ){trang}: {vang}').strip()
        if token == '':
            return None
        print('\033[1;36mĐang Xử Lý....', '     ', end='\r')
        res = login_ttc(token)
        if res is None:
            print(f'{do}Đăng Nhập Thất Bại, kiểm tra lại token!        ')
            continue
        t, ck = res
        name = ck['user']
        for i, (_, n) in enumerate(accs):
            if n == name:
                accs[i] = (token, name)
                print(f'{luc}Tài khoản {vang}{name}{luc} đã có, đã cập nhật token mới.        ')
                break
        else:
            accs.append((token, name))
            print(f'{luc}Đăng Nhập Thành Công, đã lưu tài khoản {vang}{name}        ')
        save_tokens(accs)
        return t, ck

def chon_acc(accs):
    """Chọn tài khoản đã lưu. Enter trống để quay lại. Token hết hạn thì hỏi nhập lại."""
    while True:
        raw = input(f'{thanh}{luc}Nhập Số Acc (Enter để quay lại){trang}: {vang}').strip()
        if raw == '':
            return None
        if not raw.isdigit() or not (1 <= int(raw) <= len(accs)):
            print(f'{do}Số Acc Không Tồn Tại')
            continue
        tk, name = accs[int(raw) - 1]
        print('\033[1;36mĐang Xử Lý....', '     ', end='\r')
        res = login_ttc(tk)
        if res:
            print(f'{luc}Đăng Nhập Thành Công          ')
            return res
        print(f'{do}Token của {vang}{name}{do} đã hết hạn hoặc không hợp lệ.')
        yn = input(f'{thanh}{luc}Nhập token mới cho tài khoản này? (y/n){trang}: {vang}').strip().lower()
        if yn == 'y':
            res = them_acc(accs)
            if res:
                return res

def xoa_acc(accs):
    raw = input(f'{thanh}{luc}Nhập Số Acc cần xoá (Enter để huỷ){trang}: {vang}').strip()
    if raw == '':
        return
    if raw.isdigit() and 1 <= int(raw) <= len(accs):
        _, name = accs.pop(int(raw) - 1)
        save_tokens(accs)
        print(f'{luc}Đã xoá tài khoản {vang}{name}')
    else:
        print(f'{do}Số Acc Không Tồn Tại')

def menu_token():
    """Trả về (ttc, ck) của tài khoản được chọn."""
    accs = load_tokens()
    while True:
        if not accs:
            print(f'{vang}Chưa có tài khoản TTC nào được lưu, vui lòng thêm mới.')
            res = them_acc(accs)
            if res is None:
                print(f'{do}Chưa có tài khoản nào, thoát tool.')
                sys.exit(0)
            return res

        for i, (_, name) in enumerate(accs, 1):
            print(f'{thanh}{luc}Nhập {do}[{vang}{i}{do}] {luc}Để Chạy Tài Khoản: {vang}{name}')
        print(gradient("-"*50))
        print(f'{thanh}{luc}Nhập {do}[{vang}1{do}] {luc}Chọn Acc Đã Lưu Để Chạy Tool')
        print(f'{thanh}{luc}Nhập {do}[{vang}2{do}] {luc}Thêm Access_Token TTC Mới')
        print(f'{thanh}{luc}Nhập {do}[{vang}3{do}] {luc}Xoá Acc Đã Lưu')
        print(gradient("-"*50))
        chon = input(f'{thanh}{luc}Nhập: {vang}').strip()
        print(gradient("-"*50))
        if chon == '1':
            res = chon_acc(accs)
        elif chon == '2':
            res = them_acc(accs)
        elif chon == '3':
            xoa_acc(accs)
            continue
        else:
            print(f'{do}Vui Lòng Nhập Chính Xác')
            continue
        if res:
            return res

ttc, ck = menu_token()
users, xu = ck['user'], ck['xu']

os.system("cls" if os.name == "nt" else "clear")
banner()

# ---------- MENU ----------
print(f'{thanh}{luc}TTC Name{trang}: {vang}{users}')
print(f'{thanh}{luc}Total Coin{trang}: {vang}{str(format(int(ck["xu"]),","))}')
print(gradient("-"*50))
print(f'{thanh}\033[38;2;160;231;229mNhập {do}[{vang}1{do}]\033[38;2;160;231;229m Follow Thường (subcheo)')
print(f'{thanh}\033[38;2;160;231;229mNhập {do}[{vang}2{do}]\033[38;2;160;231;229m Follow VIP (subcheovip)')
print(f'{thanh}\033[38;2;160;231;229mNhập {do}[{vang}3{do}]\033[38;2;160;231;229m Like Video (liketiktok)')
print(f'{thanh}{dep}Có Thể Chọn Nhiều Nhiệm Vụ {do}({vang}VD: 123{do})')
print(gradient("-"*50))
nhiemvu = str(input(f'{thanh}\033[38;2;220;200;255mNhập Số Để Chọn Nhiệm Vụ{trang}: {vang}'))
for x in nhiemvu:
    list_nv.append(x)
list_nv = [x for x in list_nv if x in ['1', '2', '3']]

# ---------- CẤU HÌNH ----------
print(gradient("-"*50))
print(f'{thanh}{v}→ Tool gom đủ N nhiệm vụ rồi mới nhận xu')
print(f'{thanh}{v}→ Sau delay, tự mở job mới (không cần bấm Enter)')
print(gradient("-"*50))

while True:
    try:
        so_nv_nhan = int(input(f'{thanh}{v}Số NV cần hoàn thành trước khi nhận xu (7-20){trang}: {vang}'))
        if 7 <= so_nv_nhan <= 20:
            break
        else:
            print(f'{do}Vui Lòng Nhập Từ 7 Đến 20!')
    except:
        print(f'{do}Vui Lòng Nhập Số')

def nhap_so(label, mac_dinh):
    while True:
        raw = input(f'{thanh}{v}{label} (giây, Enter = {mac_dinh}){trang}: {vang}').strip()
        if raw == '':
            return float(mac_dinh)
        try:
            val = float(raw)
            if val < 0:
                print(f'{do}Vui Lòng Nhập Số Không Âm')
                continue
            return val
        except ValueError:
            print(f'{do}Vui Lòng Nhập Số')

delay_min = nhap_so('Delay tối thiểu giữa các job', 3)
while True:
    delay_max = nhap_so('Delay tối đa giữa các job', max(delay_min, 6))
    if delay_max >= delay_min:
        break
    print(f'{do}Delay tối đa phải lớn hơn hoặc bằng delay tối thiểu ({delay_min:g}s)')

while True:
    try:
        JobbBlock = int(input(f'{thanh}{v}Sau Bao Nhiêu Nhiệm Vụ Chống Block{trang}: {vang}'))
        if JobbBlock <= 1:
            print(f'{do}Vui Lòng Nhập Lớn Hơn 1')
        break
    except:
        print(f'{do}Vui Lòng Nhập Số')

while True:
    try:
        DelayBlock = int(input(f'{thanh}{v}Sau {vang}{JobbBlock} {v}Nhiệm Vụ Nghỉ Bao Nhiêu Giây{trang}: {vang}'))
        break
    except:
        print(f'{do}Vui Lòng Nhập Số')

print(gradient("-"*50))

# ---------- VÒNG LẶP CHÍNH ----------
stt = 0
totalxu = 0
pending_jobs = []
current_field = None

while True:
    nv = random.choice(list_nv)
    if nv == '1':
        fields = 'subcheo'
        action = 'FOLLOW'
    elif nv == '2':
        fields = 'subcheovip'
        action = 'FOLLOW-VIP'
    elif nv == '3':
        fields = 'liketiktok'
        action = 'LIKE'
    else:
        continue

    # Đổi loại NV mà còn pending → nhận xu trước
    if pending_jobs and current_field and current_field != fields:
        print(f'\n{vang}→ Đổi loại NV, nhận xu {len(pending_jobs)} job cũ...')
        ok, xuthem, xu_now = ttc.nhanxu_batch(pending_jobs, current_field)
        totalxu += xuthem
        print(f'{luc}✓ Nhận {ok}/{len(pending_jobs)} job | +{format(xuthem, ",")} xu | Tổng: {format(int(xu_now), ",")}')
        pending_jobs = []
        current_field = None

    # Đủ số NV → nhận xu
    if len(pending_jobs) >= so_nv_nhan:
        print(f'\n{luc}╔══════════════════════════════════════════╗')
        print(f'{luc}║  ĐÃ ĐỦ {so_nv_nhan} NHIỆM VỤ - NHẬN XU             ║')
        print(f'{luc}╚══════════════════════════════════════════╝')
        ok, xuthem, xu_now = ttc.nhanxu_batch(pending_jobs, current_field)
        totalxu += xuthem
        print(f'{luc}✓ Nhận {ok}/{len(pending_jobs)} job | +{format(xuthem, ",")} xu | Tổng: {format(int(xu_now), ",")}')
        pending_jobs = []
        current_field = None
        continue

    try:
        getjob = ttc.getjob(fields)
        if getjob is None:
            sleep(2)
            continue

        try:
            jobs_data = getjob.json()
        except:
            print(f'{do}Response không phải JSON!', end='\r')
            sleep(3)
            continue

        if not isinstance(jobs_data, list) or len(jobs_data) == 0:
            if isinstance(jobs_data, dict) and jobs_data.get('countdown'):
                cd = jobs_data['countdown']
                print(f'{do}Tiến Hành Get Job {fields.upper()}, COUNTDOWN: {str(round(cd, 3))}', end='\r')
                sleep(1)
                Delay(cd)
            else:
                print(f'{do}{jobs_data.get("error", "Không có job")}', end='\r')
                sleep(2)
                Delay(2)
            continue

        print(luc + f" Đã Tìm Thấy {len(jobs_data)} Nhiệm Vụ {fields.title()}       ", end="\r")

        for x in jobs_data:
            if len(pending_jobs) >= so_nv_nhan:
                break

            target_user = (x.get('username') or x.get('user') or x.get('idfb')
                          or x.get('uid') or x.get('idpost', ''))
            video_url = x.get('link') or x.get('url') or ''
            job_id = x.get('id') or x.get('idpost') or target_user

            if not target_user and not video_url:
                continue

            if current_field is None:
                current_field = fields

            # Mở link
            if action in ('FOLLOW', 'FOLLOW-VIP'):
                # Ưu tiên link profile từ job (nếu có), không thì dùng username
                if video_url and 'tiktok.com' in video_url:
                    open_tiktok_profile(video_url)
                elif target_user:
                    open_tiktok_profile(target_user)
            elif action == 'LIKE':
                if video_url:
                    open_tiktok_video(video_url)

            pending_jobs.append(job_id)
            stt += 1
            id_ = target_user if target_user else video_url

            # Log kiểu TT-TOOL
            timejob = datetime.now().strftime('%H:%M:%S')
            print(f'{do}[ \033[1;36m{stt}{do} ] {do}[ {vang}TT-TOOL{do} ][ {xanh}{timejob}{do} ][ {vang}{action}{do} ][ {trang}{id_}{do} ][ {vang}+0 Xu{do} ][ {luc}{len(pending_jobs)}/{so_nv_nhan} {do}]')

            if len(pending_jobs) >= so_nv_nhan:
                break

            # Delay có hiệu ứng Doro
            if stt % int(JobbBlock) == 0:
                Delay(DelayBlock)
            else:
                Delay(random.uniform(delay_min, delay_max))

    except KeyboardInterrupt:
        if pending_jobs:
            print(f'\n{vang}Đang nhận xu cho {len(pending_jobs)} job còn lại...')
            ok, xuthem, xu_now = ttc.nhanxu_batch(pending_jobs, current_field)
            totalxu += xuthem
            print(f'{luc}✓ Nhận {ok}/{len(pending_jobs)} job | +{format(xuthem, ",")} xu | Tổng: {format(int(xu_now), ",")}')
        print(f'{vang}Đã dừng tool.')
        break
    except Exception as e:
        print(f'{do}Lỗi vòng lặp: {e}')
        sleep(2)
