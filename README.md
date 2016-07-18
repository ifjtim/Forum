Dokumentace ISJ

Stahovaní fóra

autor: Tomasz Koderla

login: xkonde03

O skriptu:

Skript je napsán v Python . Testoval jsem ho na mém notebooku Asus K50NI v operačním
systému Ubuntu 14.10 . Verze Python 2.7.8. Skript jsem spouštěl pomocí příkazu 'python forum.py'

Knihovny:

Použil jsem ve skriptu pouze jednu externí knihovnu BeautifulSoup. Tato knihovna slouží k
zpracovaní html stránky. BeautifulSoup rozkouskuje HTML stránku a vytvoří strom, který se dá
procházet. Můžeme pák najít všechny potřebné objekty html. Další knihovny které jsem používal
již sou standardní a měly by byt zabudované Python.
Forum:
Diskuzní forum z kterého jsem stahoval se jmenuje forum.autoforum.cz. Věnuje se jak jíž
název napovídat tematice automobilu. Je rozděleno do několika hlavních témat, které máji pak své
vlastni podtémata. Podtémat muže byt libovolné množství a můžou byt i na vice stranách . Každé
podtéma má již své příspěvky, kterých je také neomezené množství a můžou byt na několika
stranách.

Skript:

Skript má dvě části aktualizační, stahovací. První věc co skript udělá je, že se koukne jestli
je tam složka forum, pokud je tak aktualizuje.Po dokončeni skriptu se vypíše do konzole dokončeno
Stahovaní: skript vytvoří adresář forum a koukne se na všechny témata a vytvoří pro každé
téma také adresář. Potom stahuje příspěvky každého podtématu do souboru z jménem podtématu.
Pro stahování každého podtématu vytvoří samostatné vlákno.
Aktualizace: Skript projíždí všechny témata a podtémata pokud neekzistujou tak je stáhne.
Zároveň porovnává kolik příspěvku je stáhnuté (číslo je vždy na první řádku souboru) a kolik je
příspěvku je aktuálně v podtématu, pokud to nesedí vypočte rozdíl a přejde na poslední příspěvky a
stáhne tolik příspěvku kolik je rozdíl ve vypočtu.
Měření:
K měření jsem použil program time. Jak jsem už výše uvedl měřeni bylo prováděno na mém
notebooku. Prováděl jsem několik zkoušek tady jsou vypsaná tři měření.
stahovací
real
user
sys
52m12.932s
25m59.285s
1m49.020s
real 58m13.003s
user 26m23.191s
sys 1m57.337s
real 54m37.549s
user 25m51.470s
sys 1m54.141s
aktualizační
real
user
sys
8m54.781s
4m39.294s
2m12.782s
real
user
sys
9m24.985s
4m41.341s
2m13.460s
real 8m56.245s
user 4m39.077s
sys 2m13.056s

Zavěr:

Největší problém skriptu byl můj internet,jsem v najmu v bytě a internet tu dost padá tak
někdy se stávalo, že par vláken spadlo, protože mi spadl internet. Skript stahuje forum kolem
hodiny nejvíc zdržuje stahování dlouhých témat které mají kolem 5000 příspěvku a vice. Tento
projekt mě nátchnul je to jeden z mála projektu, které dal rozvíjet. Python jsem se učil zároveň jak
tímhle projekt a jde to vidět na kodu . Proto by byla možná úprava kodu ,pár části kodu vykonává
skoro tu samou činnost.
