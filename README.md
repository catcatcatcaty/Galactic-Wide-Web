<h1 align="center">Galactic Wide Web: Fluxer Port</h1>

<p align="center">
	<a href="https://fluxer.gg/m50i6kcZ">
		<img alt="Servers" src="https://img.shields.io/badge/servers-5+-brightgreen?style=for-the-badge">
	</a>
	<a href="https://fluxer.gg/m50i6kcZ">
		<img alt="Visible Users" src="https://img.shields.io/badge/visible users-100+-brightgreen?style=for-the-badge">
	</a>
  <br>
	<img alt="Commits made" src="https://img.shields.io/github/last-commit/catcatcatcaty/Galactic-Wide-Web?style=for-the-badge">
  <img alt="Code Size" src="https://img.shields.io/github/languages/code-size/catcatcatcaty/Galactic-Wide-Web?style=for-the-badge">
  <img alt="Code Format" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge">
  <br>
  <a href="https://ko-fi.com/R6R51OSRX8">
    <img src="https://ko-fi.com/img/githubbutton_sm.svg">
  </a>
</p>

<p align="center">
  Galactic Wide Web: Fluxer Port is a Fluxer bot for Helldivers 2 that provides real-time information on the Galactic War.
  <br>
  Disclaimer: This is a fork of the original Galactic Wide Web bot by StoneMercy. It is not feature complete and bugs are to be expected and reliability is not guaranteed. You have been warned!
  <br>
  It pulls live data from the official Helldivers 2 API and the Steam API, and keeps an auto-updating dashboard refreshed every 15 minutes with a strategic overview of the current war effort.<br><br>
  The bot includes commands, and embedded content. All interactions take place in text channels.
  <br>
  Server administrators (or those with Manage Server permissions) can configure which channels are used for dashboards and map posts.
  <br>
  Notifications can be enabled for a range of events, including:
  </p>
    <ul align="center">
    New Major Orders
    <br>
    Personal Orders
    <br>
    Dispatches
    <br>
    Global Events
    <br>
    DSS movements and Tactical Action changes
    <br>
    Planetary Region changes
    <br>
    Campaign wins and losses
    <br>
    and Steam patch notes.
    </ul>
  <p align="center">
  <br>
  The bot supports multilingual output, currently offering English, French, German, Italian, Portuguese (BR),
  <br>
  Russian, Spanish, Chinese (Traditional), and Turkish, with more languages welcome via upstream contributions.
  <br><br>
  Built using a butchered version of Disnake (ported to Fluxer), it stores settings in PostgreSQL and uses Pillow and opencv to generate maps.
</p>

## Quick Navigation
- [Inviting the Bot](#inviting-the-galactic-wide-web)
- [Examples](#examples) (to be updated)
- [Support](#support)
- [Contributing](#contributing)

## Inviting the Galactic Wide Web
Want to try out the GWW on your server? [Invite Link](https://web.fluxer.app/oauth2/authorize?client_id=1476519709822349355&scope=bot)

## Examples
### `/check_missing_translations language_to_check: pt-br`
<img src="resources/readme/check_missing_translations.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/community_servers`
<img src="resources/readme/community_servers.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/dispatches`
<img src="resources/readme/dispatches.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/dss`
![dss](resources/readme/dss.png)
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/global_events`
<img src="resources/readme/global_events.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/help command: check_missing_translations`
<img src="resources/readme/help.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/major_order`
<img src="resources/readme/major_order.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/map`
<img src="resources/readme/map.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/personal_order`
![personal_order](resources/readme/personal_order.png)
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/planet planet: 112-VERNEN WELLS`
<img src="resources/readme/planet.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/setup`
![setup](resources/readme/setup.png)
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/steam`
<img src="resources/readme/steam.png" width="500">
<p align="right"><a href="#top">Back to Top ↑</a></p>

### `/warfront faction: Terminids`
![warfront](resources/readme/warfront.png)
<p align="right"><a href="#top">Back to Top ↑</a></p>

## Support
Available here: [Fluxer Support Server](https://fluxer.gg/m50i6kcZ)
<p align="right"><a href="#top">Back to Top ↑</a></p>

## Contributing
Contributions are welcome!

To contribute to localization (upstream only):
1. Open an issue with the Language Request template
2. Create a pull request and add a .json file to the [data/languages/](https://github.com/Stonemercy/Galactic-Wide-Web/tree/main/data/languages) folder

or just head to the Fluxer Support Server above
<p align="right"><a href="#top">Back to Top ↑</a></p>
