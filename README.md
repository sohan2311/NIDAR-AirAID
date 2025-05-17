# NIDAR-AirAID

# 🛰️ IIITDM Kurnool Drone Mapping Project

This repository contains elevation data and KML files representing a detailed mapping and surveillance plan of the IIITDM Kurnool campus using Google Earth Pro. The dataset is divided into academic and residential zones, aiding in:

✅ Surveillance and geotagging  
✅ Elevation profiling  
✅ Relief operations  
✅ Campus infrastructure planning  

---

## 📁 Files Overview

| File Name                                      | Description |
|-----------------------------------------------|-------------|
| **Academic Area IIITDMK.kml**                  | Complete polygon coverage of the academic area |
| **Academic Zone Old Block.kml**                | Old academic block layout |
| **Academic Zone 1.kml**                        | Segmented path or boundary for a specific academic block |
| **Boys Hostel IIITDM K.kml**                   | Boys’ hostel boundary mapping |
| **Girls Hostel IIITDMK.kml**                   | Girls’ hostel area polygon |
| **Faculty Residence IIITDMK.kml**              | Faculty residential quarters coverage |
| **Residential Area.kml**                       | Complete residential area zone |
| **Mess Area IIITDMK.kml**                      | Polygon marking the mess/dining area |
| **CricketFootball Ground IIITDMK.kml**         | Sports ground polygon and elevation reference |
| **Sports Arena IIITDMK.kml**                   | Indoor and outdoor sports area layout |
| **Major Dhyan Chand Sports Complex IIITDMK.kml** | Detailed zone for the main sports complex |
| **Elevation - Boys Hostel.png**                | Elevation profile of Boys Hostel path |
| **Elevation - Girls Hostel.png**               | Elevation profile of Girls Hostel path |
| **Elevation - Mess.png**                       | Elevation profile of Mess area |
| **Elevation - Faculty Residence.png**          | Elevation profile of Faculty Residence area |
| **Elevation - Major Dhyan Chand Sports Complex.png** | Elevation of main sports complex |
| **Elevation - Cricket:Football Ground.png**    | Elevation profile of sports ground |
| **Elevation-Academic Zone 1.png**              | Elevation of new academic zone |
| **Elevation-Academic Zone Old Block.png**      | Elevation profile of the old block |
| **Elevation - Surveillance Path 1 - IIITDMK.png** | Planned drone route with elevation |
| **README.md**                                  | Project documentation and usage instructions |

---

## 📍 Zone Classification

### 🎓 Academic Zone
- Academic Area
- Old and New Blocks
- Surveillance Path 1

### 🏠 Residential Zone
- Boys Hostel
- Girls Hostel
- Faculty Residence
- Mess Area

### 🏟️ Utility and Sports Zones
- Sports Arena
- Cricket & Football Ground
- Dhyan Chand Sports Complex

---

## 🌍 How to Use the Files

1. **Install Google Earth Pro** (Mac/Windows/Linux)
2. **Open .kml files**:
   - `File > Open > Select KML File`
3. **View and inspect**:
   - Polygons and paths
   - Elevation profiles via:
     - `Right-click Path > Show Elevation Profile`
4. **Export elevation screenshots** for planning or simulation.

🔁 For drone mission planning (e.g., Mission Planner), convert `.kml` files to MAVLink format if necessary.

---

## 🛠 Tools Used

- **Google Earth Pro** – Drawing paths/polygons, elevation data
- **GitHub** – Version control and zone-specific branches
- **UAV Simulation Tools** – e.g., Mission Planner, QGroundControl (for future use)

---

## 🌐 Branch Organization

Each zone may have a dedicated branch:
- `academic-zone`
- `residential-zone`
- `sports-zone`
- `utilities-mapping`
- `relief-ops` *(if applicable)*

---

## 📸 Elevation Screenshots

To generate elevation screenshots:
1. Go to `Tools > Ruler > Path`
2. Draw the desired path
3. Right-click → “Show Elevation Profile”
4. Save screenshots using the format:
   - `Elevation_Academic_Path.png`
   - `Elevation_Residential_Path.png`

---

## 📜 License

Open for academic and research purposes. All zone data manually derived using public Google Earth Pro imagery. Attribution appreciated.

