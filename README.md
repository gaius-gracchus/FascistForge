Fascist Forge Scraping
======================

This repo contains scripts for scraping and analyzing the militant neo-Nazi website FascistForge.com, along with the datasets these scripts generated, in the form of both comma-separated value (\*.csv), and pickled Pandas DataFrame (\*.df).

To use these scripts, you unfortunately need to create an account on FascistForge.com.
Once you have a username and password, add them to your PATH. On Linux, you can do this by editing your ~/.bashrc to contain the following lines:

```bash
export FF_USERNAME=<your username>
export FF_PASSWORD=<your password>
```

Then, assuming you have Selenium and the other requisite packages installed and configured, you can run the scripts.