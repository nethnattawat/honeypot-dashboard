# CPE Honeypot Watch

What internet bots do to a home ONU/router that leaves **Telnet (23), SSH (22), HTTP (80, 8080) and TR-069 (7547)** open on the WAN side — recorded by a honeypot on Google Cloud (Singapore) since 2026-10-30.

บอทบน internet ทำอะไรกับ ONU/เราเตอร์บ้านที่เปิดพอร์ตจัดการไว้ฝั่ง WAN — บันทึกจาก honeypot บน Google Cloud (สิงคโปร์)

**Open the dashboard:** https://nethnattawat.github.io/honeypot-dashboard/

- Four tabs: overview, attack map (replay of real events), bot behaviour + vendor checklist, and a system diagram. Thai / English toggle at the top right.
- Data snapshot: 2026-10-30 → **2026-11-10 16:06 (Bangkok)**. The team's own test IPs are left out of every count; the honeypot's own IP is masked.
- Countries are approximated from the source IP (MaxMind GeoLite2 via geoip2fast); VPS and proxy exits show the hosting country.
- URLs and IPs inside attacker commands are defanged (`hxxp`, `[.]`). Nothing captured here should be downloaded or run.

`index.html` is a static build (`build_site.py`) of the dashboard; `data/*.json` are the five datasets it loads.
