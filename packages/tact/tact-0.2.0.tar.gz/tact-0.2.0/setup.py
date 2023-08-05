# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tact']

package_data = \
{'': ['*']}

install_requires = \
['DendroPy>=4.4,<5.0', 'click>=7.0,<8.0', 'numpy>=1.17,<2.0', 'scipy>=1.3,<2.0']

entry_points = \
{'console_scripts': ['tact_add_taxa = tact.cli_add_taxa:main',
                     'tact_build_taxonomic_tree = tact.cli_taxonomy:main',
                     'tact_check_results = tact.cli_check_trees:main']}

setup_kwargs = {
    'name': 'tact',
    'version': '0.2.0',
    'description': 'Taxonomic addition for complete trees: Adds tips to a backbone phylogeny using taxonomy simulated with birth-death models',
    'long_description': '# TACT - Taxonomy addition for complete trees\n\n[![PyPI](https://img.shields.io/pypi/v/tact.svg)](https://pypi.org/project/tact/)\n\nAdds tips to a backbone phylogeny using taxonomy simulated with birth-death models\n\n# Installation\n\nTACT requires Python 3. When possible, we recommend using the PyPy 3 implementation as it can significantly speed up TACT analyses, particularly on large datasets. In addition, TACT depends on the click, DendroPy, NumPy, and SciPy packages.\n\n## Homebrew\n\nUsing Homebrew is the recommended way to install TACT. [Install Homebrew on macOS](https://brew.sh) or [Install Homebrew on Linux or Windows 10](https://docs.brew.sh/Homebrew-on-Linux). Once Homebrew has been installed, run\n\n    brew install jonchang/biology/tact\n\n## pipx\n\nIf you are unable or unwilling to use Homebrew, the next recommended way to install TACT is via `pipx`. [Install `pipx`](https://github.com/pipxproject/pipx#install-pipx), then run:\n\n    pipx install tact\n\n## Other\n\nOther ways of installing TACT, including unpacking the tarball somewhere or directly using `pip`, are neither supported nor recommended.\n\n# Example\n\nFiles used are in the [examples](https://github.com/jonchang/tact/tree/master/examples) folder.\n\n```console\ncurl -LO https://raw.githubusercontent.com/jonchang/tact/master/examples/Carangaria.csv\ncurl -LO https://raw.githubusercontent.com/jonchang/tact/master/examples/Carangaria.tre\n```\n\nBuild a taxonomic tree using the provided CSV file. Run `tact_build_taxonomic_tree --help` to see the required format for this file.\n\n```console\n$ tact_build_taxonomic_tree Carangaria.csv --output Carangaria.taxonomy.tre\nOutput written to: Carangaria.taxonomy.tre\n```\n\n`Carangaria.taxonomy.tre` now contains a Newick phylogeny with many polytomies and named nodes indicating relevant taxonomic ranks. Now run the TACT stochastic polytomy resolver algorithm in conjunction with the backbone phylogeny `Caragaria.tre`.\n\n```console\n$ tact_add_taxa --backbone Carangaria.tre --taxonomy Carangaria.taxonomy.tre --output Carangaria.tacted --verbose --verbose\nRates  [####################################]  226/226\nTACT  [####################################]  642/642  Carangaria\n```\n\nThere will be several files created with the prefix `Carangaria.tacted`. These include `newick.tre` and `nexus.tre` (your primary output in the form of Newick and NEXUS format phylogenies), `rates.csv` (estimated diversification rates on the backbone phylogeny), and `log.txt` (extremely verbose output on what TACT is doing and why).\n\nYou should check the TACT results now for any issues:\n\n```console\n$ tact_check_results Carangaria.tacted.newick.tre --backbone Carangaria.tre --taxonomy Carangaria.taxonomy.tre > checkresults.csv\n```\n\nOpen up `checkresults.csv` in your favorite spreadsheet viewer and check the `warnings` column for any issues.\n\n# Citation\n\nThe manuscript for TACT is currently in review.\n\nTACT owes its existence to much foundational work in the area of stochastic polytomy resolution, namely PASTIS and CorSiM.\n\n* Thomas, G. H., Hartmann, K., Jetz, W., Joy, J. B., Mimoto, A., & Mooers, A. O. (2013). PASTIS: an R package to facilitate phylogenetic assembly with soft taxonomic inferences. Methods in Ecology and Evolution, 4(11), 1011–1017. doi:[10.1111/2041-210x.12117](https://doi.org/10.1111/2041-210X.12117)\n\n* Cusimano, N., Stadler, T., & Renner, S. S. (2012). A New Method for Handling Missing Species in Diversification Analysis Applicable to Randomly or Nonrandomly Sampled Phylogenies. Systematic Biology, 61(5), 785–792. doi:[10.1093/sysbio/sys031](https://doi.org/10.1093/sysbio/sys031)\n',
    'author': 'Jonathan Chang',
    'author_email': 'jonathan.chang@ucla.edu',
    'url': 'https://github.com/jonchang/tact',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
