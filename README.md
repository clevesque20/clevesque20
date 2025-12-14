- 👋 Hi, I’m @clevesque20
- 👀 I’m interested in operations✨marketing✨change management✨outdoor activities and working out✨spending time with friends
and family✨coffee, wine, pizza
- 🌱 I’m currently learning everything cybersecurity
- 💞️ I’m looking to collaborate on a website and foundation
- 📫 How to reach me- chelsea@cooperandcarmindy.com

## Downloading the latest Mail-in-a-Box release

Use the helper script in this repository to fetch the newest release archive of [Mail-in-a-Box](https://github.com/mail-in-a-box/mailinabox).

```bash
python3 scripts/download_mailinabox.py --output ./downloads
```

The command above downloads the most recent release tarball into the `downloads/` folder. If you
need a specific version, provide the release tag (for example `v60`) with the `--version` option:

```bash
python3 scripts/download_mailinabox.py --version v60 --output ./downloads
```

If the file already exists in the chosen directory the script will leave it untouched so you can
avoid unnecessary downloads.
