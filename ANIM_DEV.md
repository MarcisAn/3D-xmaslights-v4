# Kā rakstīt animācijas 3D lampiņām

## Prasības

- Python
- NodeJS
- Git (vēlams, bet var iztikt)

## Uzstādīšana

1. Lejupielādēt šo repozitoriju `git clone https://github.com/MarcisAn/3D-xmaslights-v4`
2. Palaist serveri
```
cd server
npm install
node index.js
```
3. Citā terminālī palaist vizualizētāju un atvērt to pārlūkā
```
cd visualiser
npm install
npm run dev
```
4. Nokopēt failu `generators/animations/dev.py` šajā pašā mapē un jaunajam failam piešķirt animācijas nosaukumu
5. Šo failu palaižot, animācija rādīsies vizualizācijā
6. Norādes animācijas rakstīšanai ir šajā failā
7. Nogādājiet šo python failu pie manis ar pull request vai citādi
