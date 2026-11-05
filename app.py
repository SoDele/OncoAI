<!DOCTYPE html>
<html lang="de" class="h-full bg-slate-950 text-slate-100">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OncoDictate AI | Hämatologie & Onkologie - Klinikum Kassel</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#f0fdfa',
              100: '#ccfbf1',
              500: '#14b8a6',
              600: '#0d9488',
              700: '#0f766e',
              800: '#115e59',
              900: '#134e4a',
              950: '#042f2e',
            },
            slate: {
              850: '#1e293b',
              900: '#0f172a',
              950: '#020617',
            }
          }
        }
      }
    }
  </script>
  
  <!-- FontAwesome Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  
  <style>
    /* Custom Scrollbar for Streamlit feel */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #0f172a;
    }
    ::-webkit-scrollbar-thumb {
      background: #334155;
      border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #475569;
    }

    /* Waveform Animation */
    .bar {
      transition: height 0.15s ease;
    }
    
    .pulse-red {
      animation: pulse-red 1.5s infinite;
    }
    @keyframes pulse-red {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.7; transform: scale(1.05); }
    }
  </style>
</head>
<body class="h-full font-sans antialiased bg-slate-950 text-slate-100 flex flex-col overflow-hidden">

  <!-- TOP HEADER / STREAMLIT STYLE BANNER -->
  <header class="h-14 border-b border-slate-800 bg-slate-900/90 backdrop-blur px-4 flex items-center justify-between z-20 shrink-0">
    <div class="flex items-center gap-3">
      <div class="h-8 w-8 rounded-lg bg-teal-600 flex items-center justify-center text-white font-bold text-lg shadow-md shadow-teal-900/50">
        <i class="fa-solid fa-dna"></i>
      </div>
      <div>
        <div class="flex items-center gap-2">
          <span class="font-bold text-slate-100 tracking-wide text-base">OncoDictate <span class="text-teal-400">AI</span></span>
          <span class="px-2 py-0.5 text-xs rounded-full bg-teal-500/10 text-teal-300 border border-teal-500/20 font-medium">v3.4 Oncology Edition</span>
        </div>
        <p class="text-[11px] text-slate-400">KI-Transkription & Arztbrief-Strukturierung für Hämatologie & Onkologie</p>
      </div>
    </div>

    <!-- Top Right Actions -->
    <div class="flex items-center gap-3">
      <div class="hidden md:flex items-center gap-2 bg-slate-800/80 px-3 py-1 rounded-md border border-slate-700/60 text-xs text-slate-300">
        <i class="fa-solid fa-hospital-user text-teal-400"></i>
        <span id="currentClinicBadge">Klinikum Kassel - Hämatologie & Onkologie</span>
      </div>
      <button onclick="switchTab('tab1')" class="px-3 py-1.5 bg-teal-600 hover:bg-teal-500 text-white rounded text-xs font-semibold transition flex items-center gap-2 shadow">
        <i class="fa-solid fa-microphone"></i> Neues Diktat
      </button>
    </div>
  </header>

  <!-- MAIN CONTAINER (SIDEBAR + CONTENT) -->
  <div class="flex-1 flex overflow-hidden">
    
    <!-- STREAMLIT SIDEBAR -->
    <aside class="w-80 border-r border-slate-800 bg-slate-900 flex flex-col shrink-0 overflow-y-auto">
      <div class="p-4 space-y-5">
        
        <!-- Sidebar Header -->
        <div class="border-b border-slate-800 pb-3">
          <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Konfiguration & Profil</div>
          <h2 class="text-sm font-bold text-slate-200">Arzt- & Standort-Auswahl</h2>
        </div>

        <!-- Target Institution Presets -->
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1.5">
            <i class="fa-solid fa-building-hospital mr-1.5 text-teal-400"></i>Einrichtung / Abteilung
          </label>
          <select id="presetSelect" onchange="updateInstitution()" class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-teal-500 transition">
            <option value="kassel" selected>Klinikum Kassel - Klinik für Hämatologie, Onkologie & Immunologie</option>
            <option value="nordhessen">Onkologische Schwerpunktpraxis Nordhessen</option>
            <option value="tagesklinik">Interdisziplinäre Onkologische Tagesklinik Kassel</option>
            <option value="zdf">Viszeralonkologisches Zentrum Kassel</option>
          </select>
        </div>

        <!-- Doctor Profile Selector -->
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1.5">
            <i class="fa-solid fa-user-doctor mr-1.5 text-teal-400"></i>Diktierender Arzt / Ärztin
          </label>
          <select id="doctorSelect" onchange="updateDoctorProfile()" class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-teal-500 transition">
            <option value="doerfel">Dr. med. Daniela Dörfel (Chefärztin)</option>
            <option value="ritter" selected>Barbara Ritter (Leitende Oberärztin)</option>
            <option value="sebastian">Henry Sebastian (Oberarzt)</option>
            <option value="wolf">Sebastian Wolf (Oberarzt)</option>
            <option value="barth">Volker Barth (Oberarzt)</option>
          </select>
        </div>

        <div class="border-t border-slate-800 pt-4">
          <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Dokumententyp / Modus</div>
          
          <!-- Specific Oncology Dictation Modes -->
          <div class="space-y-1.5">
            <label class="flex items-center p-2 rounded-lg bg-slate-800/50 hover:bg-slate-800 border border-slate-700/50 cursor-pointer transition">
              <input type="radio" name="docType" value="entlassung" checked onchange="setDocType('entlassung')" class="text-teal-500 focus:ring-teal-500 h-3.5 w-3.5">
              <span class="ml-2.5 text-xs font-medium text-slate-200">Stationärer Entlassbericht</span>
            </label>
            <label class="flex items-center p-2 rounded-lg bg-slate-800/50 hover:bg-slate-800 border border-slate-700/50 cursor-pointer transition">
              <input type="radio" name="docType" value="tumorboard" onchange="setDocType('tumorboard')" class="text-teal-500 focus:ring-teal-500 h-3.5 w-3.5">
              <span class="ml-2.5 text-xs font-medium text-slate-200">Tumorboard-Protokoll</span>
            </label>
            <label class="flex items-center p-2 rounded-lg bg-slate-800/50 hover:bg-slate-800 border border-slate-700/50 cursor-pointer transition">
              <input type="radio" name="docType" value="verlauf" onchange="setDocType('verlauf')" class="text-teal-500 focus:ring-teal-500 h-3.5 w-3.5">
              <span class="ml-2.5 text-xs font-medium text-slate-200">Ambulanter Verlaufsbericht</span>
            </label>
            <label class="flex items-center p-2 rounded-lg bg-slate-800/50 hover:bg-slate-800 border border-slate-700/50 cursor-pointer transition">
              <input type="radio" name="docType" value="studie" onchange="setDocType('studie')" class="text-teal-500 focus:ring-teal-500 h-3.5 w-3.5">
              <span class="ml-2.5 text-xs font-medium text-slate-200">Studien / RECIST Doku</span>
            </label>
          </div>
        </div>

        <!-- Audio Settings & KI-Feineinstellungen -->
        <div class="border-t border-slate-800 pt-4 space-y-3">
          <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Audio & KI-Optimierung</div>
          
          <div class="flex items-center justify-between text-xs text-slate-300">
            <span>Rauschunterdrückung</span>
            <input type="checkbox" checked class="toggle-checkbox accent-teal-500 rounded">
          </div>
          
          <div class="flex items-center justify-between text-xs text-slate-300">
            <span>Ambient / Freisprech-Diktat</span>
            <input type="checkbox" checked class="toggle-checkbox accent-teal-500 rounded">
          </div>

          <div class="flex items-center justify-between text-xs text-slate-300">
            <span>Auto-Strukturierung (TNM / CTCAE)</span>
            <input type="checkbox" checked class="toggle-checkbox accent-teal-500 rounded">
          </div>

          <div>
            <label class="block text-[11px] font-medium text-slate-400 mb-1">Onkologische Fachnomenklatur</label>
            <div class="flex flex-wrap gap-1">
              <span class="px-1.5 py-0.5 text-[10px] bg-slate-800 text-teal-300 rounded border border-slate-700">ICD-O-3</span>
              <span class="px-1.5 py-0.5 text-[10px] bg-slate-800 text-teal-300 rounded border border-slate-700">CTCAE v5.0</span>
              <span class="px-1.5 py-0.5 text-[10px] bg-slate-800 text-teal-300 rounded border border-slate-700">RECIST 1.1</span>
              <span class="px-1.5 py-0.5 text-[10px] bg-slate-800 text-teal-300 rounded border border-slate-700">ECOG Status</span>
            </div>
          </div>
        </div>

        <!-- System Status Banner -->
        <div class="border-t border-slate-800 pt-3">
          <div class="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1.5">
            <div class="flex items-center justify-between text-[11px]">
              <span class="text-slate-400">KIS-Anbindung (HL7/FHIR):</span>
              <span class="text-emerald-400 font-medium flex items-center gap-1"><i class="fa-solid fa-circle text-[8px]"></i> Aktiv</span>
            </div>
            <div class="flex items-center justify-between text-[11px]">
              <span class="text-slate-400">LLM Engine:</span>
              <span class="text-teal-300 font-mono">OncoLLM-v2.8</span>
            </div>
          </div>
        </div>

      </div>
    </aside>

    <!-- STREAMLIT MAIN CONTENT AREA -->
    <main class="flex-1 flex flex-col bg-slate-950 overflow-hidden">
      
      <!-- STREAMLIT TAB NAVIGATION -->
      <div class="border-b border-slate-800 bg-slate-900/60 px-6 pt-3 flex gap-2 shrink-0 overflow-x-auto">
        <button id="tab1-btn" onclick="switchTab('tab1')" class="tab-btn active px-4 py-2.5 text-xs font-semibold rounded-t-lg border-b-2 border-teal-500 text-teal-400 bg-slate-800/80 transition flex items-center gap-2">
          <i class="fa-solid fa-microphone"></i> 1. Live Diktat & KI-Transkription
        </button>
        <button id="tab2-btn" onclick="switchTab('tab2')" class="tab-btn px-4 py-2.5 text-xs font-semibold rounded-t-lg border-b-2 border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition flex items-center gap-2">
          <i class="fa-solid fa-file-medical"></i> 2. Arztbrief-Editor & Strukturierung
        </button>
        <button id="tab3-btn" onclick="switchTab('tab3')" class="tab-btn px-4 py-2.5 text-xs font-semibold rounded-t-lg border-b-2 border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition flex items-center gap-2">
          <i class="fa-solid fa-microscope"></i> 3. Tumorboard & Genetik
        </button>
        <button id="tab4-btn" onclick="switchTab('tab4')" class="tab-btn px-4 py-2.5 text-xs font-semibold rounded-t-lg border-b-2 border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition flex items-center gap-2">
          <i class="fa-solid fa-calculator"></i> 4. ROI & Zeitersparnis
        </button>
      </div>

      <!-- TAB CONTENTS CONTAINER -->
      <div class="flex-1 overflow-y-auto p-6">
        
        <!-- TAB 1: LIVE DIKTAT & KI-TRANSKRIPTION -->
        <div id="tab1" class="tab-content space-y-6">
          
          <!-- Patient Context & Header -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-wrap items-center justify-between gap-4 shadow-sm">
            <div class="flex items-center gap-4">
              <div class="h-12 w-12 rounded-full bg-teal-900/40 border border-teal-500/30 flex items-center justify-center text-teal-400 font-bold text-xl">
                <i class="fa-solid fa-user-vcard"></i>
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <h3 class="font-bold text-slate-100 text-base" id="patientNameHeader">Patient: Müller, Werner (68 J., M)</h3>
                  <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-xs border border-slate-700 font-mono">Fall-ID: 2026-88392</span>
                </div>
                <p class="text-xs text-slate-400 mt-0.5" id="patientDiagnosisSub">
                  Diagnose: Metastasiertes Adenokarzinom des Kolons (pT3 pN2a M1a - HEP), KRAS Wildtyp, PD-L1 CPS = 12
                </p>
              </div>
            </div>

            <div class="flex items-center gap-2">
              <button onclick="loadSampleCase(1)" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-xs border border-slate-700 transition flex items-center gap-1.5">
                <i class="fa-solid fa-folder-open text-teal-400"></i> Fall 1: Kolon-Ca
              </button>
              <button onclick="loadSampleCase(2)" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-xs border border-slate-700 transition flex items-center gap-1.5">
                <i class="fa-solid fa-folder-open text-teal-400"></i> Fall 2: DLBCL Lymphom
              </button>
            </div>
          </div>

          <!-- Dictation Controls & Waveform Simulation -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <!-- Left: Audio Record Controls -->
            <div class="lg:col-span-1 bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between space-y-4 shadow-sm">
              <div>
                <div class="flex items-center justify-between mb-3">
                  <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Aufnahme-Steuerung</span>
                  <span id="recordingBadge" class="hidden px-2 py-0.5 rounded-full bg-red-500/20 text-red-400 border border-red-500/30 text-[11px] font-medium flex items-center gap-1.5 pulse-red">
                    <i class="fa-solid fa-circle text-[8px]"></i> LIVE DIKTAT
                  </span>
                </div>

                <!-- Big Mic Record Button -->
                <div class="flex flex-col items-center justify-center my-4">
                  <button id="micBtn" onclick="toggleRecording()" class="w-24 h-24 rounded-full bg-teal-600 hover:bg-teal-500 text-white flex flex-col items-center justify-center shadow-lg shadow-teal-950 transition transform active:scale-95 group border-4 border-teal-700/50">
                    <i id="micIcon" class="fa-solid fa-microphone text-3xl mb-1 group-hover:scale-110 transition-transform"></i>
                    <span id="micText" class="text-[11px] font-bold uppercase tracking-wider">Start</span>
                  </button>
                  <p id="recTimer" class="mt-3 font-mono text-xl font-semibold text-slate-300">00:00</p>
                </div>

                <!-- Live Audio Visualizer Animation -->
                <div id="waveform" class="h-12 bg-slate-950 rounded-lg p-2 border border-slate-800 flex items-center justify-center gap-1 overflow-hidden opacity-50">
                  <div class="bar w-1.5 bg-teal-500 rounded-full h-2"></div>
                  <div class="bar w-1.5 bg-teal-500 rounded-full h-4"></div>
                  <div class="bar w-1.5 bg-teal-500 rounded-full h-8"></div>
                  <div class="bar w-1.5 bg-teal-500 rounded-full h-3"></div>
                  <div class="bar w-1.5 bg-teal-500 rounded-full h-6"></div>
                  <div class="bar w-1.5 bg-teal-500 rounded-full h-2"></div>
                  <div class="bar w-1.5 bg-teal-500 rounded-full h-7"></div>
                  <div class="bar w-1.5 bg-teal-500 rounded-full h-4"></div>
                  <div class="bar w-1.5 bg-teal-500 rounded-full h-2"></div>
                  <div class="bar w-1.5 bg-teal-500 rounded-full h-5"></div>
                </div>
              </div>

              <!-- Quick Audio Input Options -->
              <div class="space-y-2 border-t border-slate-800 pt-3">
                <button onclick="simulateFullDictation()" class="w-full py-2 bg-slate-800 hover:bg-slate-700 text-teal-300 rounded-lg text-xs font-semibold border border-slate-700 transition flex items-center justify-center gap-2">
                  <i class="fa-solid fa-wand-magic-sparkles"></i> Beispiel-Diktat einfügen & transkribieren
                </button>
                <div class="text-[11px] text-slate-500 text-center">
                  Nutzt spezialisiertes Onko-Whisper Modell mit Med-Vocab
                </div>
              </div>
            </div>

            <!-- Right: Realtime Speech-to-Text & Entity Recognition -->
            <div class="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between shadow-sm">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                    <i class="fa-solid fa-quote-left text-teal-400"></i> Roh-Transkript (Live Speech-to-Text)
                  </span>
                  <span class="text-[11px] text-slate-500 font-mono">Vertrauen: 98.4%</span>
                </div>

                <!-- Dictation Raw Box -->
                <div class="bg-slate-950 border border-slate-800 rounded-lg p-4 min-h-[220px] max-h-[300px] overflow-y-auto text-sm text-slate-300 font-mono leading-relaxed" id="rawTranscriptBox">
                  <span class="text-slate-600 italic">Drücken Sie "Start" oder "Beispiel-Diktat einfügen", um das Diktat zu beginnen...</span>
                </div>
              </div>

              <!-- Recognized Entities Pills -->
              <div class="border-t border-slate-800 pt-3 mt-4">
                <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2">
                  Automatisch erkannte Fachkonzepte:
                </div>
                <div id="entityPills" class="flex flex-wrap gap-1.5 min-h-[32px]">
                  <span class="text-xs text-slate-600 italic">Noch keine Entitäten extrahiert.</span>
                </div>
              </div>

              <!-- Bottom Action to Tab 2 -->
              <div class="border-t border-slate-800 pt-3 mt-4 flex justify-between items-center">
                <span class="text-xs text-slate-400">Nächster Schritt: KI-Strukturierung & Briefgenerierung</span>
                <button onclick="processAndMoveToEditor()" class="px-4 py-2 bg-teal-600 hover:bg-teal-500 text-white rounded-lg text-xs font-bold transition flex items-center gap-2 shadow">
                  Arztbrief aufbereiten <i class="fa-solid fa-arrow-right"></i>
                </button>
              </div>
            </div>

          </div>

        </div>

        <!-- TAB 2: ARZTBRIEF-EDITOR & STRUKTURIERUNG -->
        <div id="tab2" class="tab-content hidden space-y-6">
          
          <!-- Editor Header Toolbar -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-wrap items-center justify-between gap-3 shadow-sm">
            <div class="flex items-center gap-3">
              <span class="text-xs font-bold text-slate-300 uppercase tracking-wider">Generierter Entwurf:</span>
              <span id="docTypeTag" class="px-2.5 py-1 rounded-md bg-teal-500/10 text-teal-300 border border-teal-500/30 text-xs font-medium">
                Stationärer Entlassungsbericht
              </span>
            </div>

            <div class="flex items-center gap-2">
              <button onclick="regenerateReport()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-xs border border-slate-700 transition flex items-center gap-1.5">
                <i class="fa-solid fa-arrows-rotate text-teal-400"></i> Neu strukturieren
              </button>
              <button onclick="copyToClipboard()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-xs border border-slate-700 transition flex items-center gap-1.5">
                <i class="fa-solid fa-copy text-teal-400"></i> Kopieren
              </button>
              <button onclick="exportHL7()" class="px-3 py-1.5 bg-teal-600 hover:bg-teal-500 text-white rounded text-xs font-semibold transition flex items-center gap-1.5 shadow">
                <i class="fa-solid fa-file-export"></i> KIS Export (HL7/FHIR)
              </button>
            </div>
          </div>

          <!-- Structured Sections Editor -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <!-- Main Medical Letter Text Area -->
            <div class="lg:col-span-2 space-y-4">
              
              <!-- Section 1: Diagnosen & Staging -->
              <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-2">
                <div class="flex items-center justify-between">
                  <label class="text-xs font-bold text-teal-400 uppercase tracking-wider flex items-center gap-2">
                    <i class="fa-solid fa-disease"></i> Haupt- & Nebendiagnosen (incl. TNM / Staging)
                  </label>
                  <span class="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded">ICD-10-GM</span>
                </div>
                <textarea id="secDiagnoses" rows="4" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-slate-200 font-mono leading-relaxed focus:border-teal-500 focus:outline-none transition"></textarea>
              </div>

              <!-- Section 2: Anamnese, B-Symptomatik & ECOG -->
              <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-2">
                <label class="text-xs font-bold text-teal-400 uppercase tracking-wider flex items-center gap-2">
                  <i class="fa-solid fa-notes-medical"></i> Anamnese, B-Symptomatik & ECOG-Status
                </label>
                <textarea id="secAnamnesis" rows="3" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-slate-200 font-mono leading-relaxed focus:border-teal-500 focus:outline-none transition"></textarea>
              </div>

              <!-- Section 3: Chemotherapie / Systemtherapie-Zyklen -->
              <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-2">
                <label class="text-xs font-bold text-teal-400 uppercase tracking-wider flex items-center gap-2">
                  <i class="fa-solid fa-pills"></i> Verabreichte Systemtherapie & Nebenwirkungen (CTCAE)
                </label>
                <textarea id="secTherapy" rows="4" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-slate-200 font-mono leading-relaxed focus:border-teal-500 focus:outline-none transition"></textarea>
              </div>

              <!-- Section 4: Befunde (CT/PET-CT/RECIST) & Labor -->
              <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-2">
                <label class="text-xs font-bold text-teal-400 uppercase tracking-wider flex items-center gap-2">
                  <i class="fa-solid fa-x-ray"></i> Apparative Befunde, Tumoransprechen & Labor
                </label>
                <textarea id="secFindings" rows="4" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-slate-200 font-mono leading-relaxed focus:border-teal-500 focus:outline-none transition"></textarea>
              </div>

              <!-- Section 5: Procedere & Empfehlungen -->
              <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-2">
                <label class="text-xs font-bold text-teal-400 uppercase tracking-wider flex items-center gap-2">
                  <i class="fa-solid fa-clipboard-check"></i> Weiteres Procedere & Supportivtherapie
                </label>
                <textarea id="secProcedere" rows="4" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-slate-200 font-mono leading-relaxed focus:border-teal-500 focus:outline-none transition"></textarea>
              </div>

            </div>

            <!-- Sidebar Info & Validation Checks -->
            <div class="lg:col-span-1 space-y-4">
              
              <!-- KI Quality & Safety Check -->
              <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
                <div class="flex items-center justify-between border-b border-slate-800 pb-2">
                  <span class="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center gap-1.5">
                    <i class="fa-solid fa-shield-halved text-emerald-400"></i> KI-Vollständigkeits-Check
                  </span>
                  <span class="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-bold">100% Ok</span>
                </div>

                <div class="space-y-2 text-xs">
                  <div class="flex items-center justify-between text-slate-300">
                    <span class="flex items-center gap-2"><i class="fa-solid fa-check text-emerald-400"></i> TNM / Staging klassifiziert</span>
                    <i class="fa-solid fa-circle-check text-emerald-400"></i>
                  </div>
                  <div class="flex items-center justify-between text-slate-300">
                    <span class="flex items-center gap-2"><i class="fa-solid fa-check text-emerald-400"></i> ECOG Status erfasst</span>
                    <i class="fa-solid fa-circle-check text-emerald-400"></i>
                  </div>
                  <div class="flex items-center justify-between text-slate-300">
                    <span class="flex items-center gap-2"><i class="fa-solid fa-check text-emerald-400"></i> CTCAE Toxizität spezifiziert</span>
                    <i class="fa-solid fa-circle-check text-emerald-400"></i>
                  </div>
                  <div class="flex items-center justify-between text-slate-300">
                    <span class="flex items-center gap-2"><i class="fa-solid fa-check text-emerald-400"></i> Neutropenie-Prophylaxe / G-CSF</span>
                    <i class="fa-solid fa-circle-check text-emerald-400"></i>
                  </div>
                </div>
              </div>

              <!-- Brief Kopf & Unterschriften Block Preview -->
              <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
                <div class="text-xs font-bold text-slate-200 uppercase tracking-wider border-b border-slate-800 pb-2">
                  Briefkopf & Freigabe
                </div>
                
                <div class="text-[11px] space-y-2 text-slate-400">
                  <div>
                    <span class="text-slate-500 block">Klinik:</span>
                    <span class="text-slate-200 font-medium" id="previewClinic">Klinikum Kassel - Klinik für Hämatologie, Onkologie & Immunologie</span>
                  </div>
                  <div>
                    <span class="text-slate-500 block">Verantwortlicher Oberarzt / Chefarzt:</span>
                    <span class="text-slate-200 font-medium" id="previewDoctor">Barbara Ritter (Leitende Oberärztin)</span>
                  </div>
                  <div>
                    <span class="text-slate-500 block">Freigabe-Status:</span>
                    <span class="inline-block mt-0.5 px-2 py-0.5 bg-amber-500/20 text-amber-300 border border-amber-500/30 rounded text-[10px]">Entwurf zur Ärztlichen Unterschrift</span>
                  </div>
                </div>

                <button onclick="alert('Arztbrief wurde erfolgreich signiert und an das KIS übermittelt!')" class="w-full mt-2 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold transition flex items-center justify-center gap-2 shadow">
                  <i class="fa-solid fa-signature"></i> Final Signieren & Speichern
                </button>
              </div>

            </div>

          </div>

        </div>

        <!-- TAB 3: TUMORBOARD & GENETIK -->
        <div id="tab3" class="tab-content hidden space-y-6">
          
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <h3 class="text-sm font-bold text-slate-100 flex items-center gap-2">
                  <i class="fa-solid fa-users-rectangle text-teal-400"></i> Multidisziplinäres Tumorboard - Protokoll-Generator
                </h3>
                <p class="text-xs text-slate-400">Molekularpathologie, NGS-Mutationen & Interdisziplinäre Therapie-Empfehlung</p>
              </div>
              <span class="px-3 py-1 rounded-full bg-teal-500/20 text-teal-300 border border-teal-500/30 text-xs font-medium">
                Interdisziplinäres Zentrum Kassel
              </span>
            </div>

            <!-- NGS Mutation Matrix -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-3">
              <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                <span class="text-[10px] text-slate-500 uppercase font-semibold">KRAS Status</span>
                <p class="text-xs font-bold text-emerald-400 mt-1">Wildtyp (Exon 2,3,4)</p>
              </div>
              <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                <span class="text-[10px] text-slate-500 uppercase font-semibold">BRAF Status</span>
                <p class="text-xs font-bold text-emerald-400 mt-1">V600E Negativ</p>
              </div>
              <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                <span class="text-[10px] text-slate-500 uppercase font-semibold">MSI / MMR Status</span>
                <p class="text-xs font-bold text-slate-200 mt-1">MSS (Mikrosatellitenstabil)</p>
              </div>
              <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                <span class="text-[10px] text-slate-500 uppercase font-semibold">PD-L1 Expression</span>
                <p class="text-xs font-bold text-teal-400 mt-1">CPS = 12 (Positiv)</p>
              </div>
            </div>

            <!-- Interdisciplinary Consensus Output -->
            <div class="space-y-3 pt-2">
              <label class="block text-xs font-bold text-slate-300">
                Tumorboard-Beschluss & Therapielinien-Empfehlung:
              </label>
              <textarea id="tbConsensus" rows="6" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-slate-200 font-mono leading-relaxed focus:border-teal-500 focus:outline-none transition">
Empfehlung des Molekularen Tumorboards am Klinikum Kassel:
1. Fortführung der Palliative Systemtherapie der 1. Linie mit mFOLFOX6 in Kombination mit Panitumumab (EGFR-Antikörper) bei nachgewiesenem KRAS Wildtyp.
2. Re-Evaluation mittels Kontrastmittel-CT (Chest/Abdomen) nach 4 weiteren Therapiezyklen (ca. 8 Wochen).
3. Bei gutem Ansprechen erneute Vorstellung in der Viszeralchirurgischen Konferenz bzgl. Option einer sekundären Lebermetastasen-Resektion.
4. Molekulares Re-Staging via Liquid Biopsy bei Progress empfohlen.
              </textarea>
            </div>

            <div class="flex justify-end gap-2">
              <button onclick="alert('Tumorboard-Protokoll wurde an alle Teilnehmer & KIS gesendet!')" class="px-4 py-2 bg-teal-600 hover:bg-teal-500 text-white rounded-lg text-xs font-bold transition flex items-center gap-2">
                <i class="fa-solid fa-share-nodes"></i> Beschluss im KIS freigeben & verteilen
              </button>
            </div>
          </div>

        </div>

        <!-- TAB 4: ROI & ZEITERSPARNIS-RECHNER -->
        <div id="tab4" class="tab-content hidden space-y-6">
          
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
            <div>
              <h3 class="text-base font-bold text-slate-100 flex items-center gap-2">
                <i class="fa-solid fa-calculator text-teal-400"></i> Effizienz & ROI-Rechner (Onkologie Spezifisch)
              </h3>
              <p class="text-xs text-slate-400">Kalkulation der Zeitersparnis bei komplexen onkologischen Entlassberichten & Chemotherapie-Dokumentationen</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
              
              <!-- Sliders Panel -->
              <div class="space-y-5 bg-slate-950 p-5 rounded-xl border border-slate-800">
                
                <div>
                  <div class="flex justify-between text-xs font-semibold mb-2">
                    <span class="text-slate-300">Anzahl Ärzte / Onkologen:</span>
                    <span class="text-teal-400 font-mono text-sm" id="valDoctors">8</span>
                  </div>
                  <input type="range" id="sliderDoctors" min="1" max="30" value="8" oninput="calculateROI()" class="w-full accent-teal-500">
                </div>

                <div>
                  <div class="flex justify-between text-xs font-semibold mb-2">
                    <span class="text-slate-300">Arztbriefe / Berichte pro Arzt pro Tag:</span>
                    <span class="text-teal-400 font-mono text-sm" id="valLetters">4</span>
                  </div>
                  <input type="range" id="sliderLetters" min="1" max="15" value="4" oninput="calculateROI()" class="w-full accent-teal-500">
                </div>

                <div>
                  <div class="flex justify-between text-xs font-semibold mb-2">
                    <span class="text-slate-300">Dauer pro Brief (Bisher manuell):</span>
                    <span class="text-amber-400 font-mono text-sm" id="valTimeOld">18 Min</span>
                  </div>
                  <input type="range" id="sliderTimeOld" min="10" max="35" value="18" oninput="calculateROI()" class="w-full accent-amber-500">
                </div>

                <div>
                  <div class="flex justify-between text-xs font-semibold mb-2">
                    <span class="text-slate-300">Dauer mit OncoDictate AI:</span>
                    <span class="text-emerald-400 font-mono text-sm" id="valTimeNew">3.5 Min</span>
                  </div>
                  <input type="range" id="sliderTimeNew" min="1" max="10" value="3.5" step="0.5" oninput="calculateROI()" class="w-full accent-emerald-500">
                </div>

              </div>

              <!-- ROI Results Output Box -->
              <div class="flex flex-col justify-between space-y-4">
                
                <div class="grid grid-cols-1 gap-4">
                  
                  <div class="bg-teal-950/40 border border-teal-500/30 p-5 rounded-xl">
                    <span class="text-xs text-teal-300 font-semibold uppercase tracking-wider block mb-1">Zeitersparnis pro Brief</span>
                    <div class="text-3xl font-extrabold text-teal-400 font-mono" id="savedPerLetter">14.5 Min</div>
                    <span class="text-[11px] text-slate-400 mt-1 block">Reduktion der Dokumentationszeit um ~80%</span>
                  </div>

                  <div class="bg-slate-950 border border-slate-800 p-5 rounded-xl">
                    <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider block mb-1">Eingesparte Arbeitszeit (Gesamtes Team / Jahr)</span>
                    <div class="text-3xl font-extrabold text-slate-100 font-mono" id="savedHoursYear">2.436 Std.</div>
                    <span class="text-[11px] text-slate-400 mt-1 block">Entspricht ca. 1.3 Vollzeit-Arztstellen (FTE) für die Patientenversorgung</span>
                  </div>

                  <div class="bg-emerald-950/40 border border-emerald-500/30 p-5 rounded-xl">
                    <span class="text-xs text-emerald-300 font-semibold uppercase tracking-wider block mb-1">Geschätzte monetäre Effizienzsteigerung</span>
                    <div class="text-3xl font-extrabold text-emerald-400 font-mono" id="savedEuroYear">170.520 € / Jahr</div>
                    <span class="text-[11px] text-slate-400 mt-1 block">Basierend auf durchschnittlichem Ärztlichen Stundensatz</span>
                  </div>

                </div>

              </div>

            </div>
          </div>

        </div>

      </div>

    </main>

  </div>

  <!-- JAVASCRIPT LOGIC & SAMPLE DATA -->
  <script>
    // Sample Data Sets for Oncology Cases
    const sampleCases = {
      1: {
        headerName: "Müller, Werner (68 J., M)",
        headerSub: "Diagnose: Metastasiertes Adenokarzinom des Kolons (pT3 pN2a M1a - HEP), KRAS Wildtyp, PD-L1 CPS = 12",
        transcript: "Diktat für den Patienten Werner Müller, geboren 14.05.1958. Aufnahme zur Durchführung des 4. Zyklus einer chemotherapeutischen Systemtherapie nach dem mFOLFOX6 Schema in Kombination mit Panitumumab bei metastasiertem Kolonkarzinom. Anamnestisch gab der Patient eine B-Symptomatik mit leichtem Gewichtsverlust an, ECOG Status aktuell 1. Bei der Aufnahme zeigte sich im Labor eine mäßige Neutropenie Grad 2 mit 1200 Neutrophilen, Hämoglobin bei 10.4 g/dl. Wir führten die Chemo nach Dosisanpassung und Gabe von Supportiva durch. Im Kontroll-CT zeigt sich eine partielle Remission der hepatischen Filiae nach RECIST 1.1. Weiteres Procedere: Empfehlung zur Fortführung von Zyklus 5 in zwei Wochen, engmaschige Blutbildkontrolle sowie Prophylaxe mit G-CSF bei Bedarf.",
        entities: [
          { name: "Metastasiertes Kolonkarzinom", type: "Diagnosis" },
          { name: "mFOLFOX6 + Panitumumab", type: "Therapy" },
          { name: "ECOG Status 1", type: "Score" },
          { name: "CTCAE Grade 2 Neutropenie", type: "Toxicity" },
          { name: "RECIST 1.1 Partielle Remission", type: "Response" },
          { name: "G-CSF Supportiv", type: "Supportive" }
        ],
        diagnoses: "1. Metastasierte Adenokarzinom des Sigmakolons (ICD-10 C18.7)\n   - TNM: pT3 pN2a M1a (HEP), L1 V1 Pn0, G2\n   - Molekulargenetik: KRAS Wildtyp, BRAF Wildtyp, MSS, PD-L1 CPS = 12\n2. Chemotherapie-induzierte Neutropenie CTCAE Grad 2\n3. Anämie Grad 1 (Hb 10.4 g/dl)",
        anamnesis: "Patient stellt sich zum 4. Zyklus mFOLFOX6 + Panitumumab vor. Subjektiv gutes Befinden, geringe Fatigue (Grad 1). Keine ausgeprägte B-Symptomatik. ECOG Performance Status: 1.",
        therapy: "Durchführung des 4. Zyklus mFOLFOX6 (Oxaliplatin, 5-FU, Folinsäure) + Panitumumab (6 mg/kg) am 02.11.2026. Gute Verträglichkeit. Nebenwirkungen: Mäßiges papulopustulöses Hautexanthem Grad 1 unter Panitumumab, Neutropenie Grad 2.",
        findings: "Re-Staging CT Thorax/Abdomen vom 28.10.2026: Regress der bekannten Lebermetastasen in Segment V und VIII im Sinne einer Partiellen Remission (PR) nach RECIST 1.1 criteria (-34% Summe der Zieldurchmesser). Kein Nachweis neuer Filiae.",
        procedere: "1. Fortführung der Systemtherapie mit Zyklus 5 am 16.11.2026 in unserer Interdisziplinären Tagesklinik.\n2. Supportiv: Fortführung der Hautpflege mit Doxycyclin-Salbe.\n3. Laborkontrolle (Differenzialblutbild) in 1 Woche beim Hausarzt.\n4. Wiedervorstellung im Tumorboard nach 6 Zyklen zur Prüfung der Resektabilität."
      },
      2: {
        headerName: "Kaufmann, Sabine (54 J., W)",
        headerSub: "Diagnose: Diffuses großzelliges B-Zell-Lymphom (DLBCL), Ann-Arbor Stadium III E, IPI 3",
        transcript: "Diktat für Frau Sabine Kaufmann. Stationäre Entlassung nach 3. Zyklus R-CHOP-21 Immunchemotherapie bei de novo DLBCL. Patientin zeigt exzellentes Ansprechen. B-Symptomatik mit Nachtschweiß ist nach dem 1. Zyklus komplett sistiert. ECOG Status verbessert von 2 auf 0. Das Zwischen-PET/CT nach Zyklus 2 ergab ein Ansprechen mit Deauville Score 2. Labor bei Entlassung: Leukozyten 4.200, Thrombozyten normwertig. Procedere: Geplant sind insgesamt 6 Zyklen R-CHOP gefolgt von einer intrathekalen ZNS-Prophylaxe mit Methotrexat.",
        entities: [
          { name: "DLBCL Lymphom", type: "Diagnosis" },
          { name: "Ann-Arbor Stadium III E", type: "Staging" },
          { name: "R-CHOP-21 Schema", type: "Therapy" },
          { name: "Deauville Score 2", type: "PET Response" },
          { name: "ECOG Status 0", type: "Score" },
          { name: "ZNS-Prophylaxe i.th.", type: "Supportive" }
        ],
        diagnoses: "1. Diffuses großzelliges B-Zell-Lymphom (DLBCL), B-Zell-Typ (ICD-10 C83.3)\n   - Ann-Arbor Stadium III E\n   - IPI (International Prognostic Index): 3 (Intermediär-High)\n   - B-Symptomatik bei Erstdiagnose positive, aktuell regredient",
        anamnesis: "54-jährige Patientin zur stationären Durchführung des 3. Zyklus R-CHOP-21. B-Symptomatik (Nachtschweiß, Fieber) komplett sistiert. Allgemeinzustand deutlich verbessert. ECOG: 0.",
        therapy: "Verabreichung von Zyklus 3 R-CHOP (Rituximab, Cyclophosphamid, Doxorubicin, Vincristin, Prednisolon) ohne kardiale oder infektiöse Komplikationen. Pre-Medikation mit Clemastin und Dexamethason.",
        findings: "Zwischen-PET/CT nach 2 Zyklen R-CHOP: Vollständige metabolische Remission der cervicalen und iliaren Lymphknotenkonlomerate (Deauville Score 2). Echokardiographie: LVEF 62% erhalten.",
        procedere: "1. Ambulante Aufnahme für Zyklus 4 R-CHOP am 20.11.2026.\n2. Durchführung der 2. intrathekalen MTX-Gabe zur ZNS-Prophylaxe.\n3. Weiterführung der Infektionsprophylaxe mit Cotrimoxazol und Aciclovir."
      }
    };

    let isRecording = false;
    let recInterval = null;
    let recSeconds = 0;

    // Tab Switching Logic
    function switchTab(tabId) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(el => {
        el.classList.remove('active', 'border-teal-500', 'text-teal-400', 'bg-slate-800/80');
        el.classList.add('border-transparent', 'text-slate-400');
      });

      document.getElementById(tabId).classList.remove('hidden');
      const activeBtn = document.getElementById(tabId + '-btn');
      activeBtn.classList.add('active', 'border-teal-500', 'text-teal-400', 'bg-slate-800/80');
      activeBtn.classList.remove('border-transparent', 'text-slate-400');
    }

    // Load Sample Case
    function loadSampleCase(caseId) {
      const data = sampleCases[caseId];
      document.getElementById('patientNameHeader').innerText = "Patient: " + data.headerName;
      document.getElementById('patientDiagnosisSub').innerText = "Diagnose: " + data.headerSub;
      
      // Raw transcript
      document.getElementById('rawTranscriptBox').innerText = data.transcript;

      // Entity Pills
      const pillsContainer = document.getElementById('entityPills');
      pillsContainer.innerHTML = '';
      data.entities.forEach(ent => {
        const span = document.createElement('span');
        span.className = 'px-2 py-1 text-xs bg-teal-950/80 text-teal-300 border border-teal-500/40 rounded-md font-medium flex items-center gap-1';
        span.innerHTML = `<i class="fa-solid fa-tag text-[10px] text-teal-400"></i> ${ent.name} <span class="text-[9px] text-slate-400">(${ent.type})</span>`;
        pillsContainer.appendChild(span);
      });

      // Fill Tab 2 Inputs
      document.getElementById('secDiagnoses').value = data.diagnoses;
      document.getElementById('secAnamnesis').value = data.anamnesis;
      document.getElementById('secTherapy').value = data.therapy;
      document.getElementById('secFindings').value = data.findings;
      document.getElementById('secProcedere').value = data.procedere;
    }

    // Toggle Audio Recording Simulation
    function toggleRecording() {
      const micBtn = document.getElementById('micBtn');
      const micText = document.getElementById('micText');
      const micIcon = document.getElementById('micIcon');
      const badge = document.getElementById('recordingBadge');
      const waveform = document.getElementById('waveform');

      if (!isRecording) {
        isRecording = true;
        micBtn.classList.remove('bg-teal-600', 'hover:bg-teal-500');
        micBtn.classList.add('bg-red-600', 'hover:bg-red-500');
        micText.innerText = "Stopp";
        micIcon.className = "fa-solid fa-square text-3xl mb-1";
        badge.classList.remove('hidden');
        waveform.classList.remove('opacity-50');

        recSeconds = 0;
        recInterval = setInterval(() => {
          recSeconds++;
          const mins = String(Math.floor(recSeconds / 60)).padStart(2, '0');
          const secs = String(recSeconds % 60).padStart(2, '0');
          document.getElementById('recTimer').innerText = `${mins}:${secs}`;
          
          // Animate bars
          document.querySelectorAll('.bar').forEach(bar => {
            bar.style.height = Math.floor(Math.random() * 28 + 4) + 'px';
          });
        }, 200);

      } else {
        isRecording = false;
        micBtn.classList.remove('bg-red-600', 'hover:bg-red-500');
        micBtn.classList.add('bg-teal-600', 'hover:bg-teal-500');
        micText.innerText = "Start";
        micIcon.className = "fa-solid fa-microphone text-3xl mb-1";
        badge.classList.add('hidden');
        waveform.classList.add('opacity-50');
        clearInterval(recInterval);

        // Auto load structured sample
        simulateFullDictation();
      }
    }

    function simulateFullDictation() {
      loadSampleCase(1);
    }

    function processAndMoveToEditor() {
      switchTab('tab2');
    }

    // Institution and Profile Handlers
    function updateInstitution() {
      const select = document.getElementById('presetSelect');
      const text = select.options[select.selectedIndex].text;
      document.getElementById('currentClinicBadge').innerText = text;
      document.getElementById('previewClinic').innerText = text;
    }

    function updateDoctorProfile() {
      const select = document.getElementById('doctorSelect');
      const text = select.options[select.selectedIndex].text;
      document.getElementById('previewDoctor').innerText = text;
    }

    function setDocType(type) {
      const typeMap = {
        'entlassung': 'Stationärer Entlassungsbericht',
        'tumorboard': 'Tumorboard-Protokoll & Empfehlung',
        'verlauf': 'Ambulanter Chemotherapie-Verlaufsbericht',
        'studie': 'Studien- & RECIST Dokumentation'
      };
      document.getElementById('docTypeTag').innerText = typeMap[type] || 'Arztbrief';
    }

    // ROI Calculator
    function calculateROI() {
      const doctors = parseInt(document.getElementById('sliderDoctors').value);
      const letters = parseInt(document.getElementById('sliderLetters').value);
      const timeOld = parseFloat(document.getElementById('sliderTimeOld').value);
      const timeNew = parseFloat(document.getElementById('sliderTimeNew').value);

      document.getElementById('valDoctors').innerText = doctors;
      document.getElementById('valLetters').innerText = letters;
      document.getElementById('valTimeOld').innerText = timeOld + " Min";
      document.getElementById('valTimeNew').innerText = timeNew + " Min";

      const savedPerBrief = timeOld - timeNew;
      document.getElementById('savedPerLetter').innerText = savedPerBrief.toFixed(1) + " Min";

      // 220 working days per year
      const totalLettersYear = doctors * letters * 220;
      const totalMinutesSaved = totalLettersYear * savedPerBrief;
      const totalHoursSaved = Math.round(totalMinutesSaved / 60);

      document.getElementById('savedHoursYear').innerText = totalHoursSaved.toLocaleString('de-DE') + " Std.";

      // Assume 70 EUR/hour average physician cost
      const euroSaved = Math.round(totalHoursSaved * 70);
      document.getElementById('savedEuroYear').innerText = euroSaved.toLocaleString('de-DE') + " € / Jahr";
    }

    function copyToClipboard() {
      const text = `KLINIK: ${document.getElementById('previewClinic').innerText}\nARZT: ${document.getElementById('previewDoctor').innerText}\n\nDIAGNOSEN:\n${document.getElementById('secDiagnoses').value}\n\nANAMNESE:\n${document.getElementById('secAnamnesis').value}\n\nTHERAPIE:\n${document.getElementById('secTherapy').value}\n\nBEFUNDE:\n${document.getElementById('secFindings').value}\n\nPROCEDERE:\n${document.getElementById('secProcedere').value}`;
      navigator.clipboard.writeText(text);
      alert("Arztbrief in die Zwischenablage kopiert!");
    }

    function exportHL7() {
      alert("HL7 FHIR DocumentReference Payload wurde generiert und an das KIS übertragen!");
    }

    function regenerateReport() {
      alert("KI strukturiert den Arztbrief neu basierend auf den aktuellen Einstellungen...");
    }

    // Initialize Default Case on Load
    window.onload = function() {
      loadSampleCase(1);
      calculateROI();
    };
  </script>
</body>
</html>
