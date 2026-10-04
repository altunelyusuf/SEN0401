"""Fetch the latest-release data of the toolkits the book lists from their package registries (SEN0401 chapter 03).
Writes ch03-evidence/registry_toolkits_v1_1_0.json: one entry per toolkit with the registry, the latest version and its date."""
import json, urllib.request, datetime, sys
UA = {"User-Agent": "sen0401-course-evidence (altunel.yusuf@gmail.com)"}
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)
out = {"queried": datetime.date.today().isoformat(), "entries": {}}
def put(name, registry, url, fn):
    try:
        v, d = fn(get(url)); out["entries"][name] = {"registry": registry, "url": url, "latest": v, "date": d}
    except Exception as e:
        out["entries"][name] = {"registry": registry, "url": url, "error": repr(e)}
def npm(j): v = j["dist-tags"]["latest"]; return v, j["time"][v][:10]
def pypi(j): v = j["info"]["version"]; return v, j["releases"][v][0]["upload_time"][:10]
put("bcoin", "npm", "https://registry.npmjs.org/bcoin", npm)
put("bitcore-lib", "npm", "https://registry.npmjs.org/bitcore-lib", npm)
put("bitcoinjs-lib", "npm", "https://registry.npmjs.org/bitcoinjs-lib", npm)
put("python-bitcoinlib", "PyPI", "https://pypi.org/pypi/python-bitcoinlib/json", pypi)
put("pycoin", "PyPI", "https://pypi.org/pypi/pycoin/json", pypi)
put("btcd", "Go module proxy", "https://proxy.golang.org/github.com/btcsuite/btcd/@latest", lambda j: (j["Version"], j["Time"][:10]))
put("rust-bitcoin", "crates.io", "https://crates.io/api/v1/crates/bitcoin", lambda j: (j["crate"]["max_stable_version"], j["crate"]["updated_at"][:10]))
put("bitcoinj", "Maven Central", "https://search.maven.org/solrsearch/select?q=g:org.bitcoinj+AND+a:bitcoinj-core&rows=1&wt=json",
    lambda j: (j["response"]["docs"][0]["latestVersion"], datetime.datetime.fromtimestamp(j["response"]["docs"][0]["timestamp"] / 1000, datetime.UTC).date().isoformat()))
put("bitcoin-s", "Maven Central", "https://search.maven.org/solrsearch/select?q=g:org.bitcoin-s+AND+a:bitcoin-s-core_2.13&rows=1&wt=json",
    lambda j: (j["response"]["docs"][0]["latestVersion"], datetime.datetime.fromtimestamp(j["response"]["docs"][0]["timestamp"] / 1000, datetime.UTC).date().isoformat()))
put("NBitcoin", "NuGet", "https://api.nuget.org/v3-flatcontainer/nbitcoin/index.json", lambda j: (j["versions"][-1], None))
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "ch03-evidence/registry_toolkits_v1_1_0.json", "w"), indent=1)
print(json.dumps(out, indent=1))
