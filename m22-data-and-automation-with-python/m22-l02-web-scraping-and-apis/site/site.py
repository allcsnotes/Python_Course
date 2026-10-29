"""A local stand-in for the public allcsvideos.com, for the course. Standard library only.
Site on port 22280 (HTML pages), API on port 22281 (JSON, needs a token). Nothing here talks to the internet."""
import json, os, threading, time
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

TOKEN = os.environ.get('ALLCS_TOKEN', 'demo-token-4f2a9c')
TITLES = """Python: From Zero to Production|1499|Beginner|120|4.8|9120
Python Data Structures Made Simple|799|Beginner|42|4.6|5310
Git and GitHub for Beginners|499|Beginner|28|4.5|7420
SQL and Postgres in Docker|899|Intermediate|36|4.7|4210
FastAPI from Scratch|999|Intermediate|40|4.7|3980
Docker for Python Apps|799|Intermediate|30|4.6|3540
Redis and Caching in Practice|699|Intermediate|24|4.4|2210
Testing with pytest|599|Intermediate|26|4.8|3890
Clean Code and Refactoring|649|Intermediate|22|4.5|2760
Async Python Without Fear|899|Advanced|34|4.6|1980
System Design: URL Shortener|1199|Advanced|18|4.7|2640
System Design: Chat Application|1199|Advanced|20|4.6|2105
Java: From Zero to Spring Boot|1499|Beginner|110|4.7|8310
Spring Boot REST APIs|999|Intermediate|38|4.6|3720
Spring Security Basics|849|Advanced|27|4.3|1630
Data Structures and Algorithms in C++|1399|Intermediate|96|4.8|6240
Dynamic Programming Patterns|749|Advanced|32|4.7|3010
Graph Algorithms Step by Step|749|Advanced|30|4.6|2480
Linux Command Line Basics|399|Beginner|20|4.5|6120
Bash Scripting for Developers|549|Intermediate|24|4.4|2390
Kubernetes in Plain English|1099|Advanced|44|4.5|2870
AWS Cloud Practitioner Prep|899|Beginner|36|4.4|4550
Terraform Essentials|949|Intermediate|31|4.5|2010
CI/CD with GitHub Actions|699|Intermediate|22|4.6|3330
HTML and CSS Crash Course|349|Beginner|18|4.3|8120
JavaScript for Absolute Beginners|599|Beginner|46|4.6|7210
React Fundamentals|899|Intermediate|40|4.7|5680
TypeScript in Real Projects|799|Intermediate|28|4.5|3460
Machine Learning Taster|1099|Intermediate|35|4.4|3920
Data Analysis with pandas|849|Intermediate|29|4.7|4380
Interview Preparation Roadmap|499|Beginner|16|4.8|9870
Competitive Programming Habits|649|Advanced|25|4.5|1890""".split('\n')
COURSES = []
for i, row in enumerate(TITLES, 1):
    t, p, lv, ls, r, st = row.split('|')
    slug = ''.join(c if c.isalnum() else '-' for c in t.lower()).strip('-')
    while '--' in slug: slug = slug.replace('--', '-')
    COURSES.append(dict(id=i, slug=slug, title=t, price=int(p), level=lv, lessons=int(ls), rating=float(r), students=int(st)))
PER = 8
PAGES = (len(COURSES) + PER - 1) // PER
LIVE = [('Ask Meera Anything: Python', 'Sat 19:00'), ('Live Code Review: FastAPI', 'Sun 18:00'), ('Docker Office Hours', 'Tue 20:00'), ('Mock Interview Night', 'Thu 21:00'), ('SQL Q and A', 'Fri 19:30')]

CSS = """body{font-family:Arial,Helvetica,sans-serif;background:#f6f8fb;margin:0;color:#14213d}
header{background:#0d1b3e;color:#fff;padding:18px 40px;display:flex;align-items:center;justify-content:space-between}
header b{font-size:26px} header a{color:#9fc4ff;margin-left:26px;text-decoration:none;font-size:18px}
main{max-width:1100px;margin:28px auto;padding:0 24px}
h1{font-size:34px;margin:0 0 20px}
.course{background:#fff;border:1px solid #d9e1ee;border-radius:12px;padding:16px 22px;margin-bottom:14px;display:flex;align-items:center;gap:20px}
.course .title{margin:0;font-size:24px;flex:1}.course .title a{color:#14213d;text-decoration:none}
.price{font-weight:700;font-size:22px;color:#0b6b3a;width:120px}.level{background:#e6efff;border-radius:20px;padding:5px 14px;font-size:16px;width:110px;text-align:center}
.rating{font-size:18px;width:60px}
.pager{margin:22px 0;font-size:20px}.pager a{color:#1a56db;margin-right:18px}
ul.live{list-style:none;padding:0}ul.live li{background:#fff;border:1px solid #d9e1ee;border-radius:12px;padding:16px 22px;margin-bottom:12px;font-size:22px}
.card{display:flex;gap:20px;align-items:center;background:#fff;border:2px solid #cdd8ec;border-radius:16px;padding:16px 22px;margin-bottom:14px;list-style:none}
.card-title{margin:0;font-size:24px;flex:1}.card-price{font-weight:700;font-size:22px;color:#a3410a}.card-level{font-size:16px}
"""

def page(title, body, base=''):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head>
<body><header><b>allcsvideos</b><nav><a href="{base}/">Home</a><a href="{base}/courses">Courses</a><a href="/live">Live</a></nav></header>
<main>{body}</main></body></html>"""

def course_html(c):
    return (f'  <div class="course" data-id="{c["id"]}">\n'
            f'    <h2 class="title"><a href="/courses/{c["slug"]}">{c["title"]}</a></h2>\n'
            f'    <span class="price">Rs {c["price"]}</span>\n'
            f'    <span class="level">{c["level"]}</span>\n'
            f'    <span class="rating">{c["rating"]}</span>\n'
            f'  </div>')

def list_page(n, new=False):
    sub = COURSES[(n - 1) * PER:n * PER]
    base = '/new' if new else ''
    if not new:
        items = '\n'.join(course_html(c) for c in sub)
        nxt = f'<a class="next" href="/courses?page={n + 1}">Next page</a>' if n < PAGES else ''
        prv = f'<a class="prev" href="/courses?page={n - 1}">Previous page</a>' if n > 1 else ''
        body = f'<h1>All courses</h1>\n{items}\n<div class="pager">{prv} {nxt}<span>Page {n} of {PAGES}</span></div>'
    else:
        items = '\n'.join(f'  <li class="card"><h3 class="card-title"><a href="/courses/{c["slug"]}">{c["title"]}</a></h3>'
                          f'<div class="card-price">Rs {c["price"]}</div><div class="card-level">{c["level"]}</div></li>' for c in sub)
        nxt = f'<a rel="next" href="/new/courses?page={n + 1}">More</a>' if n < PAGES else ''
        body = f'<h1>All courses</h1>\n<ul style="padding:0">\n{items}\n</ul>\n<div class="pager">{nxt}<span>Page {n} of {PAGES}</span></div>'
    return page('All courses · allcsvideos', body, base)

LIVEPAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Live sessions · allcsvideos</title><style>%s</style></head>
<body><header><b>allcsvideos</b><nav><a href="/">Home</a><a href="/courses">Courses</a><a href="/live">Live</a></nav></header>
<main><h1>Live sessions this week</h1>
<p id="status">Loading...</p>
<ul class="live" id="sessions"></ul>
<script>
setTimeout(function () {
  fetch('/live-sessions.json').then(function (r) { return r.json(); }).then(function (data) {
    var ul = document.getElementById('sessions');
    data.forEach(function (s) {
      var li = document.createElement('li');
      li.className = 'session';
      li.textContent = s.title + ' - ' + s.when;
      ul.appendChild(li);
    });
    document.getElementById('status').textContent = data.length + ' sessions';
  });
}, 700);
</script></main></body></html>""" % CSS

HITS = defaultdict(deque); LOCK = threading.Lock(); LIMIT, WINDOW, RETRY = 3, 2.0, 2

def limited(ip):
    now = time.time()
    with LOCK:
        q = HITS[ip]
        while q and now - q[0] > WINDOW: q.popleft()
        if len(q) >= LIMIT: return True
        q.append(now); return False

class Site(BaseHTTPRequestHandler):
    server_version = 'allcsvideos-copy'
    def log_message(self, fmt, *a): print(time.strftime('%H:%M:%S'), 'site', self.client_address[0], fmt % a, flush=True)
    def send(self, code, body, ctype='text/html; charset=utf-8', extra=None):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(code); self.send_header('Content-Type', ctype); self.send_header('Content-Length', str(len(b)))
        for k, v in (extra or {}).items(): self.send_header(k, v)
        self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        u = urlparse(self.path); path = u.path; q = parse_qs(u.query)
        if path in ('/courses', '/new/courses') or path.startswith('/courses/'):
            if limited(self.client_address[0]):
                return self.send(429, page('Slow down', '<h1>429 Too Many Requests</h1><p>You are asking too fast. Please wait a moment and try again.</p>'), extra={'Retry-After': str(RETRY)})
        if path == '/robots.txt':
            return self.send(200, 'User-agent: *\nDisallow: /admin/\nCrawl-delay: 1\n', 'text/plain; charset=utf-8')
        if path == '/':
            return self.send(200, page('allcsvideos', '<h1>Learn to code, step by step</h1><p style="font-size:22px">%d courses. <a href="/courses">See all courses</a></p>' % len(COURSES)))
        if path in ('/courses', '/new/courses'):
            try: n = int(q.get('page', ['1'])[0])
            except ValueError: n = 0
            if not 1 <= n <= PAGES: return self.send(404, page('Not found', '<h1>404 No such page</h1>'))
            return self.send(200, list_page(n, new=path.startswith('/new')))
        if path.startswith('/courses/'):
            slug = path.split('/')[2]
            for c in COURSES:
                if c['slug'] == slug:
                    return self.send(200, page(c['title'], f'<h1>{c["title"]}</h1><p style="font-size:22px">Rs {c["price"]} · {c["level"]} · {c["lessons"]} lessons · rated {c["rating"]}</p>'))
            return self.send(404, page('Not found', '<h1>404 No such course</h1>'))
        if path.startswith('/admin/'):
            return self.send(200, page('Admin', '<h1>Admin: students</h1><p>This page is for staff only. robots.txt asks robots to stay out.</p>'))
        if path == '/live': return self.send(200, LIVEPAGE)
        if path == '/live-sessions.json':
            time.sleep(0.4)
            return self.send(200, json.dumps([{'title': t, 'when': w} for t, w in LIVE]), 'application/json')
        return self.send(404, page('Not found', '<h1>404 Not found</h1>'))

class Api(BaseHTTPRequestHandler):
    server_version = 'allcsvideos-api-copy'
    def log_message(self, fmt, *a): print(time.strftime('%H:%M:%S'), 'api ', self.client_address[0], fmt % a, flush=True)
    def send(self, code, obj, extra=None):
        b = json.dumps(obj).encode()
        self.send_response(code); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(b)))
        for k, v in (extra or {}).items(): self.send_header(k, v)
        self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        u = urlparse(self.path); q = parse_qs(u.query)
        if self.headers.get('Authorization') != 'Bearer ' + TOKEN:
            return self.send(401, {'detail': 'Missing or wrong token'}, {'WWW-Authenticate': 'Bearer'})
        if u.path == '/api/courses':
            try: limit = max(1, min(int(q.get('limit', ['10'])[0]), 50)); offset = max(0, int(q.get('offset', ['0'])[0]))
            except ValueError: return self.send(422, {'detail': 'limit and offset must be numbers'})
            host = self.headers.get('Host', 'localhost:22281')
            nxt = f'http://{host}/api/courses?limit={limit}&offset={offset + limit}' if offset + limit < len(COURSES) else None
            res = [{k: c[k] for k in ('id', 'title', 'price', 'level', 'lessons', 'rating', 'students')} for c in COURSES[offset:offset + limit]]
            return self.send(200, {'count': len(COURSES), 'next': nxt, 'results': res})
        return self.send(404, {'detail': 'Not found'})

def serve(cls, port): ThreadingHTTPServer(('0.0.0.0', port), cls).serve_forever()
if __name__ == '__main__':
    threading.Thread(target=serve, args=(Api, 22281), daemon=True).start()
    print('site on 22280, api on 22281,', len(COURSES), 'courses', flush=True)
    serve(Site, 22280)
