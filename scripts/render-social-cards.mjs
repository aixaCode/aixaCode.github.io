// Render native SVG card templates; artwork stays untouched inside the template.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const sharp=require(process.env.SHARP_MODULE || 'sharp');
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const escape=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const font=await fs.readFile(path.join(root,'site/assets/fonts/instrument-serif-latin.woff2'));
const sans=await fs.readFile(path.join(root,'site/assets/fonts/dm-sans-latin.woff2'));
const metrics=JSON.parse(await fs.readFile(path.join(root,'design/social-font-metrics.json'),'utf8'));
const textWidth=s=>[...s].reduce((sum,c)=>sum+(metrics[c]??0.6),0)*56;
const essays=JSON.parse(await fs.readFile(path.join(root,'content/essays.json'),'utf8'));
const cards=[...essays,{slug:'og-default',title:'Engineering, with perspective.',image:'engineering-notebook-v2.webp'}];
await fs.mkdir(path.join(root,'design/social-cards'),{recursive:true});
for(const card of cards){
 const artwork=await fs.readFile(path.join(root,'site/assets/images',card.image || `${card.slug}-editorial-${card.slug==='make-improvement-plans-winnable'?'v4':'v3'}.webp`));
 const image=await sharp(artwork).png().toBuffer();
 const words=card.title.split(/\s+/);let line='';const lines=[];
 for(const word of words){if(line && textWidth(line+' '+word)>540){lines.push(line);line=word;}else line+=(line?' ':'')+word;}if(line)lines.push(line);
 const fontsize=lines.length>4?48:56,leading=fontsize+8;
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="630" viewBox="0 0 1200 630"><defs><style>@font-face{font-family:Heading;src:url(data:font/woff2;base64,${font.toString('base64')})}@font-face{font-family:Body;src:url(data:font/woff2;base64,${sans.toString('base64')})}</style></defs><rect width="1200" height="630" fill="#fff8ef"/><path d="M60 105 H1140" stroke="#d9c6b7"/><text x="60" y="73" fill="#a04637" font-family="Body,Arial" font-size="24" letter-spacing="2">THE NOTEBOOK / AGNIESZKA BESZ</text>${lines.map((l,i)=>`<text x="60" y="${190+i*leading}" fill="#4c332c" font-family="Heading,Georgia" font-size="${fontsize}">${escape(l)}</text>`).join('')}<image xlink:href="data:image/png;base64,${image.toString('base64')}" x="645" y="143" width="495" height="355" preserveAspectRatio="xMidYMid meet"/><text x="60" y="545" font-size="23" font-family="Body,Arial" fill="#765d51">Engineering / Product / Leadership</text><text x="1140" y="565" text-anchor="end" font-size="30" font-family="Body,Arial" fill="#a04637">besz.me</text></svg>`;
 const name=card.slug==='og-default'?'og-default-v4':`${card.slug}-og-v4`;
 await fs.writeFile(path.join(root,'design/social-cards',`${name}.svg`),svg);
 await sharp(Buffer.from(svg)).jpeg({quality:90}).toFile(path.join(root,'site/assets/images',`${name}.jpg`));
}
console.log(`Rendered ${cards.length} social cards`);
