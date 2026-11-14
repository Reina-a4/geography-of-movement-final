"""Chapter 02: interactive IOM-documented origin/destination associations.
The map displays selected precisely transcribed records, not a comprehensive total.
Location plotting uses indicative town-center coordinates, not IOM GPS coordinates.
"""
from pathlib import Path
import json
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

ROOT=Path(__file__).resolve().parent.parent
SOURCE='https://dtm.iom.int/reports/mobility-snapshot-round-7-26-10-2023'
CSV=ROOT/'data'/'iom_round7_selected_routes.csv'

st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
.stApp,[data-testid="stAppViewContainer"]{background:#101820!important;color:#F5F0E8}
.block-container{max-width:1440px;padding-top:1.2rem;padding-bottom:3rem}
[data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none!important}
[data-testid="stToolbar"]{visibility:hidden}
.ch-two-topline{color:#D6AA76;letter-spacing:.16em;font:600 12px Inter,Arial,sans-serif}
.ch-two-title{color:#F5F0E8;font:normal clamp(32px,4.5vw,55px)/1.14 Georgia,serif;margin:10px 0 10px}
.ch-two-sub{color:#B8C7CC;font:400 15px/1.65 Inter,Arial,sans-serif;max-width:830px;margin:0 0 19px}
.ch-two-accent{color:#79B7B5}
.stButton button{background:#1B3036!important;color:#F5F0E8!important;border:1px solid #426068!important;border-radius:9px!important}
.stButton button:hover{border-color:#D6AA76!important;color:#D6AA76!important}
</style>
""")

if st.button('← Home', key='ch2_home_button_final'):
    # The homepage is registered as a st.Page in app.py.
    home = st.session_state.get('gom_home_page')
    if home is not None:
        st.switch_page(home)
    else:
        st.error('Open the website from app.py to use the Home navigation.')

st.html('''<div class="ch-two-topline">CHAPTER 02 · FOLLOW THE MOVEMENT · IOM 2023</div>
<div class="ch-two-title">Trace the Journey</div>
<p class="ch-two-sub">A place on a report is not necessarily a journey. Here, the evidence goes further: <span class="ch-two-accent">IOM records both an area of origin and a reported location of displacement.</span> Choose a city on the map to draw its documented connections.</p>''')

if not CSV.exists():
    st.error('Chapter 2 data is missing. Please extract the entire Chapter 2 ZIP into your geography-of-movement folder.')
    st.stop()

df=pd.read_csv(CSV)
needed={'origin','destination','reported_idps','origin_lat','origin_lon','destination_lat','destination_lon','source_page'}
if not needed.issubset(df.columns):
    st.error('Chapter 2 data file is missing columns: '+str(sorted(needed-set(df.columns))))
    st.stop()
records=df.to_dict(orient='records')
data_json=json.dumps(records,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')

page=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1" />
<link rel="preconnect" href="https://unpkg.com"><link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<style>
*{box-sizing:border-box}body{margin:0;background:#101820;color:#F5F0E8;font-family:Inter,Arial,sans-serif}
.layout{display:grid;grid-template-columns:minmax(0,1.65fr) minmax(300px,1fr);gap:17px;align-items:stretch}
.card{background:#16262D;border:1px solid #34505A;border-radius:14px;overflow:hidden}
.mapcard{position:relative;min-height:580px;background:#101E26}
#map{height:580px;width:100%;background:#E6E9E6}
.info-chip{position:absolute;z-index:700;left:18px;top:16px;border:1px solid #415964;background:rgba(16,24,32,.93);border-radius:9px;padding:11px 13px;color:#CEDBD9;font-size:12px;line-height:1.6;pointer-events:none}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:7px}.teal{background:#087D84}.amber{background:#A72D54}
/* Only the basemap is desaturated; data markers and drawn routes retain their colors. */
/* Neutral context basemap: apply to tile images, not data SVG overlays. */
.leaflet-tile-pane{filter:grayscale(1) saturate(0) brightness(1.18) contrast(.66)!important}
.leaflet-tile-pane img.leaflet-tile{filter:grayscale(1) saturate(0)!important}

.leaflet-container{background:#E6E9E6!important;font-family:Inter,Arial,sans-serif}
.leaflet-control-attribution{background:rgba(16,24,32,.85)!important;color:#CCD8DB!important;font-size:9px!important}
.leaflet-control-attribution a{color:#D6AA76!important}.leaflet-control-zoom a{background:#1D3039!important;color:#F5F0E8!important;border-color:#35525C!important}
.leaflet-tooltip{background:#13242B;color:#F5F0E8;border:1px solid #48636B;border-radius:8px;box-shadow:none;font-size:12px}
.leaflet-tooltip:before{display:none}
.side{display:flex;flex-direction:column;gap:15px;min-width:0}
.panel{padding:20px 22px}.eyebrow{color:#D6AA76;letter-spacing:.13em;text-transform:uppercase;font-weight:700;font-size:11px}
h2{font:normal 25px Georgia,serif;margin:9px 0 10px}.desc{color:#B9CACC;font-size:13px;line-height:1.55;margin:0}
select{display:block;width:100%;margin-top:14px;background:#21363F;color:#F5F0E8;border:1px solid #45616B;border-radius:9px;padding:12px 12px;font:500 13px Inter,Arial,sans-serif;outline:none}
.kpis{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin-top:14px}
.kpi{border:1px solid #37525C;border-radius:10px;background:#1B3038;padding:12px}
.kpi b{font:normal 29px Georgia,serif;color:#D6AA76;display:block}.kpi span{font-size:11px;color:#B9C8CB;line-height:1.3}
.subhead{font:normal 19px Georgia,serif;color:#F5F0E8;margin:0 0 13px}
#routeList{max-height:244px;overflow:auto;scrollbar-color:#4A636B #15262D}
.route{width:100%;border:0;border-bottom:1px solid #2B414A;background:transparent;color:#F5F0E8;text-align:left;padding:11px 3px;cursor:pointer;display:flex;gap:10px;align-items:center;justify-content:space-between}
.route:hover,.route.active{background:#243941}.route .journey{font-size:12px;line-height:1.4;color:#D8E4E2;min-width:0}.route .count{flex-shrink:0;color:#D6AA76;font-size:13px;font-weight:700}
.empty{color:#91A9AF;font-size:13px;line-height:1.6;padding:20px 2px}
.foot{color:#AFC0C3;font-size:11px;line-height:1.65;margin-top:12px}
.note{margin-top:14px;padding:12px 14px;border-left:3px solid #79B7B5;background:#1B3036;color:#C4D5D5;font-size:12px;line-height:1.6}
.leaflet-interactive:focus{outline:2px solid #D6AA76;outline-offset:2px}
.status{color:#79B7B5;font-size:12px;margin-top:7px}
@media(max-width:820px){.layout{grid-template-columns:1fr}.mapcard,#map{min-height:370px;height:370px}.panel{padding:17px}.side{gap:12px}}
</style></head><body>
<div class="layout">
 <section class="card mapcard"><div id="map" aria-label="Interactive map with clickable origin and destination circles"></div>
 <div class="info-chip"><div><span class="dot amber"></span> Destination</div><div><span class="dot teal"></span> Origin</div><div style="margin-top:5px;color:#D6AA76">Click a city to reveal connections</div></div></section>
 <div class="side">
  <section class="card panel"><div class="eyebrow">YOUR INVESTIGATION CONTINUES</div><h2>Where did people go?</h2><p class="desc">Select a destination or origin. Its recorded connections will draw across the map—one by one.</p>
   <select id="citySelect" aria-label="Choose an origin or destination"><option value="">Choose a city or locality…</option></select>
   <div id="status" class="status">No city selected yet.</div>
   <div class="kpis"><div class="kpi"><b id="routeCount">—</b><span>Documented records in selection</span></div><div class="kpi"><b id="peopleCount">—</b><span>Sum of IDPs in selected records*</span></div></div>
  </section>
  <section class="card panel"><h3 class="subhead">Connections from the evidence</h3><div id="routeList"><div class="empty">Click a teal origin or amber destination marker to reveal its reported connections.</div></div>
   <div class="note">*These are <strong>selected rows</strong> from the 2023 IOM report, not all displaced people in Lebanon. A line connects reported origin and displacement location; it is <strong>not a traced travel route</strong>.</div>
  </section>
 </div>
</div>
<p class="foot">Source: IOM Displacement Tracking Matrix, <em>Mobility Snapshot – Round 7</em>, published 26 October 2023, data collected through 23 October 2023, selected transcribed rows from pp. 2–4. Points use <strong>approximate town-centre locations</strong> for illustration because IOM tables provide locality names rather than GPS coordinates. Some origin information in the full report is missing and is excluded here. Map tiles require internet access.</p>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const records=__RECORDS__;
const $=id=>document.getElementById(id);
const fmt=x=>Number(x).toLocaleString('en-US');
const cityData=new Map();
records.forEach((r,i)=>{
 if(!cityData.has('d:'+r.destination))cityData.set('d:'+r.destination,{name:r.destination,role:'destination',lat:r.destination_lat,lon:r.destination_lon});
 if(!cityData.has('o:'+r.origin))cityData.set('o:'+r.origin,{name:r.origin,role:'origin',lat:r.origin_lat,lon:r.origin_lon});
});
const destinations=[...cityData].filter(([k,v])=>v.role==='destination').map(([key,v])=>({key,...v})).sort((a,b)=>a.name.localeCompare(b.name));
const origins=[...cityData].filter(([k,v])=>v.role==='origin').map(([key,v])=>({key,...v})).sort((a,b)=>a.name.localeCompare(b.name));
const choice=$('citySelect');
const optgroup=(label,cities)=>{const group=document.createElement('optgroup');group.label=label;cities.forEach(c=>{const o=document.createElement('option');o.value=c.key;o.textContent=c.name;group.appendChild(o)});choice.appendChild(group)};
optgroup('DESTINATIONS',destinations);optgroup('ORIGINS',origins);
let map,routeLayer,markerLayer,allMarkers=[],selectedKey='',selectedRoute=-1;
function reportList(rows){
 $('routeCount').textContent=rows.length?fmt(rows.length):'—';
 $('peopleCount').textContent=rows.length?fmt(rows.reduce((a,b)=>a+Number(b.reported_idps),0)):'—';
 let sorted=[...rows].sort((a,b)=>b.reported_idps-a.reported_idps);
 if(!sorted.length){$('routeList').innerHTML='<div class="empty">Select a city on the map or use the menu to start.</div>';return}
 $('routeList').innerHTML='';
 sorted.forEach(r=>{const b=document.createElement('button');b.className='route';const id=records.indexOf(r);b.dataset.id=id;
 const nm=document.createElement('span');nm.className='journey';nm.textContent=r.origin+'  →  '+r.destination;
 const count=document.createElement('span');count.className='count';count.textContent=fmt(r.reported_idps);
 b.append(nm,count);b.title='Highlight this connection (IOM page '+r.source_page+')';b.onclick=()=>focusRoute(id);$('routeList').append(b)});
}
function niceCurve(a,b,index){
 const p=L.latLng(a[0],a[1]),q=L.latLng(b[0],b[1]);
 const x=(p.lat+q.lat)/2,y=(p.lng+q.lng)/2;
 const dx=q.lng-p.lng,dy=q.lat-p.lat;
 const curvature=Math.min(.035,Math.hypot(dx,dy)*.075)*(index%2===0?1:-1);
 const mid=[x+dx*curvature,y-dy*curvature];
 return [p,L.latLng(mid[0],mid[1]),q];
}
let paths=[];
function animatePath(line,delay=0){
 requestAnimationFrame(()=>{const p=line._path;if(!p)return;const length=p.getTotalLength();p.style.strokeDasharray=length+' '+length;p.style.strokeDashoffset=length;p.style.transition='none';requestAnimationFrame(()=>{p.style.transition='stroke-dashoffset 850ms ease '+delay+'ms';p.style.strokeDashoffset='0'})});
}
function focusRoute(id){
 selectedRoute=id;
 document.querySelectorAll('.route').forEach(el=>el.classList.toggle('active',+el.dataset.id===id));
 paths.forEach(item=>item.line.setStyle({weight:item.id===id?4:1.9,opacity:item.id===id?1:.20,color:item.id===id?'#F5A837':'#F0A542'}));
 const r=records[id]; if(r && map)map.fitBounds([[r.origin_lat,r.origin_lon],[r.destination_lat,r.destination_lon]],{padding:[95,95],maxZoom:10,animate:true});
 $('status').textContent=r.origin+' → '+r.destination+' · '+fmt(r.reported_idps)+' reported IDPs';
}
function selectCity(key){
 if(!cityData.has(key))return;
 const info=cityData.get(key);selectedKey=key;choice.value=key;selectedRoute=-1;
 const rows=records.filter(r=>info.role==='destination'?r.destination===info.name:r.origin===info.name);
 $('status').textContent=info.name+' · '+(info.role==='destination'?'destination':'origin')+' · '+rows.length+' connections';
 reportList(rows);
 if(!map)return;
 routeLayer.clearLayers();paths=[];
 allMarkers.forEach(({marker,key:k,role})=>marker.setStyle({radius:k===key?9:(role==='destination'?6.5:4.5),weight:k===key?3:1,fillOpacity:k===key?1:(role==='destination'?1:.85)}));
 const bounds=[];
 rows.forEach((r,i)=>{const coords=niceCurve([r.origin_lat,r.origin_lon],[r.destination_lat,r.destination_lon],i);
 const line=L.polyline(coords,{color:'#F0A542',weight:2.2,opacity:.75,interactive:true,lineCap:'round'}).addTo(routeLayer);
 line.bindTooltip(r.origin+' → '+r.destination+' · '+fmt(r.reported_idps)+' reported IDPs',{sticky:true});
 const rid=records.indexOf(r);line.on('click',()=>focusRoute(rid));paths.push({line,id:rid});
 bounds.push([r.origin_lat,r.origin_lon],[r.destination_lat,r.destination_lon]);
 });
 const draw=()=>paths.forEach((p,i)=>animatePath(p.line,Math.min(i*75,1400)));
 if(bounds.length){map.fitBounds(bounds,{padding:[55,55],maxZoom:10,animate:true});setTimeout(draw,600)}
}
choice.onchange=()=>{if(choice.value)selectCity(choice.value);else {selectedKey='';reportList([]);$('status').textContent='No city selected yet.';if(routeLayer)routeLayer.clearLayers()}};
if(typeof L==='undefined'){
 $('map').innerHTML='<div style="padding:80px 35px;color:#F5F0E8;line-height:2"><h2>Map needs an internet connection</h2><p>The interactive map library could not load. Check your connection and refresh this page.</p></div>';
}else{
 map=L.map('map',{zoomControl:true,scrollWheelZoom:false,preferCanvas:false}).fitBounds([[33.05,35.05],[34.75,36.65]]);
 // OpenStreetMap's public tiles do not require a CARTO API key.
 const base=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{
   attribution:'© OpenStreetMap contributors', maxZoom:18, crossOrigin:true
 }).addTo(map);
 // Set visual treatment on ONLY the tile pane, never on routes or markers.
 const tilePane=map.getPane('tilePane');
 if(tilePane){tilePane.style.filter='grayscale(1) saturate(0) brightness(1.18) contrast(.66)';}
 let tilesFailed=0;
 base.on('tileerror',()=>{
   tilesFailed++;
   if(tilesFailed===3 && !$('mapTileNotice')){
     const n=document.createElement('div');n.id='mapTileNotice';
     n.textContent='Map background could not load. Check your internet connection; route markers remain available.';
     n.style.cssText='position:absolute;bottom:28px;left:14px;right:14px;background:#152833e8;color:#f5f0e8;padding:10px;z-index:701;border:1px solid #61767d;border-radius:6px;font:12px Arial';
     $('map').appendChild(n);
   }
 });
 routeLayer=L.layerGroup().addTo(map);markerLayer=L.layerGroup().addTo(map);
 // Origins underneath destinations so clicking an overlapping destination remains possible.
 origins.forEach(c=>{let marker=L.circleMarker([c.lat,c.lon],{radius:4.5,color:'#004D54',weight:1.6,fillColor:'#087D84',fillOpacity:.85}).addTo(markerLayer);
 marker.bindTooltip('Origin · '+c.name,{direction:'top'});marker.on('click',()=>selectCity(c.key));allMarkers.push({marker,key:c.key,role:'origin'})});
 destinations.forEach(c=>{let marker=L.circleMarker([c.lat,c.lon],{radius:6.5,color:'#6F183B',weight:1.6,fillColor:'#A72D54',fillOpacity:1}).addTo(markerLayer);
 marker.bindTooltip('Destination · '+c.name,{direction:'top'});marker.on('click',()=>selectCity(c.key));allMarkers.push({marker,key:c.key,role:'destination'})});
 setTimeout(()=>map.invalidateSize(),160);
}
</script></body></html>'''
page=page.replace('__RECORDS__',data_json)
components.html(page,height=750,scrolling=True)
st.caption('**A note on interpretation:** Chapter 1 uses AUB PKGCubes observations across 2023–2024. This chapter uses a separate IOM snapshot dated 26 October 2023. They are not directly comparable totals.')
st.markdown(f'[Read the IOM source report]({SOURCE})')
