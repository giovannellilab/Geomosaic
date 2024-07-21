# Devel Integration

Welcome to our section of Contributes. If you are here, maybe you enjoyed Geomosaic and you would like to have a package/module of your interest integrated into the tool. You are in the right place (we hope!!). I think that through this guide you will be able to integrate what you want without breaking anything!

Let's jump it in.

Currently, we only accept packages that can be installed through **some channel of conda** like [Bioconda](https://bioconda.github.io/) or [Conda-Forge](https://conda-forge.org/packages/). We do not accept any package that for example can be installed by compiling the source code or package described through Dockerfile or (any type of containerization).
Is not because we don't want, but because we didn't try that way. However, if you know a way how to do it using conda env, please contact us or open an issue explaining your strategy.

At the time of writing there are three example of integration:
- [Simple package](simplepackage.md), which reagard an integration of a program that doesn't need an **external database** and it is **not referred to MAGs module**.
- [Extdb](extdb), which regard an integration of a program that requires an **external database** and it is **not referred to MAGs module**.
- [MAGs package](magspackage), which regard an integration of a program that requires an **external database** and it is **referred to MAGs module**.

However, before going further in the example guides, we suggest you to get familiar with the [meaning of the Modules](../modules.md#description).


