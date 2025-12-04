// Translations
const translations = {
    no: {
        'hero-badge': 'Oppdatert desember 2025',
        'version-badge': 'v2.1.0',
        'hero-subtitle': 'Månedlig rangering av AI-verktøy basert på buzz, sentiment og nytteverdi',
        'new-this-month': 'Ny denne måneden',
        'biggest-changes': 'Største endringer',
        'metrics-title': 'Slik leser du dataene',
        'metric-buzz': 'Hvor mye modellen/verktøyet diskuteres (0–100)',
        'metric-sentiment': 'Hvor positivt/negativt det omtales i communityet',
        'metric-utility': 'Opplevd praktisk nytteverdi',
        'metric-price': 'Opplevd kost/nytte (lavere = bedre verdi)',
        'label-utility': 'Nytte',
        'label-price': 'Pris',
        'filter-label': 'Filtrer etter kategori:',
        'filter-all': 'Alle',
        'cat-core-llm': 'Kjerne-LLM-er',
        'cat-code': 'Kodeassistenter',
        'cat-image': 'Bilde & Video',
        'cat-audio': 'Lyd & Stemme',
        'cat-agents': 'Agenter & Automatisering',
        'models': 'modeller',
        'tools': 'verktøy',
        'platforms': 'plattformer',
        'cta-title': 'Vil du bruke AI mer effektivt i teamet ditt?',
        'cta-text': 'FYRK hjelper bedrifter å velge riktige verktøy og bygge AI-drevne arbeidsflyter.',
        'cta-button': 'Kontakt oss',
        'contact': 'Kontakt',
        'last-updated': 'Sist oppdatert: 4. des 2025',
        'show-all': 'Vis alle',
        'show-fewer': 'Vis færre',
        'tab-scores': 'Rankings',
        'tab-capabilities': 'Model Abilities',
        'lab-badge': '🧪 FYRK Lab',
        'lab-text': 'Et eksperiment – ikke en benchmark.',
        'les-mer': 'Les mer',
        'close': 'Lukk',
        'capabilities-title': 'Kapabiliteter',
        'capabilities-subtitle': 'Hva kan hver modell?',
        'legend-best': 'Best',
        'legend-yes': 'Ja',
        'legend-partial': 'Delvis',
        'legend-no': 'Nei',
        'cap-header-cognitive': 'Cognitive abilities',
        'cap-reasoning': 'Reasoning',
        'cap-coding': 'Coding',
        'cap-memory': 'Memory (context)',
        'cap-multilingual': 'Multilingual / Norwegian',
        'cap-header-visual': 'Visual abilities',
        'cap-image-gen': 'Image generation',
        'cap-image-understanding': 'Image understanding',
        'cap-video-gen': 'Video generation',
        'cap-video-understanding': 'Video understanding',
        'cap-header-audio': 'Audio & speech',
        'cap-speech-to-text': 'Speech-to-text',
        'cap-text-to-speech': 'Text-to-speech',
        'cap-audio-understanding': 'Audio understanding',
        'cap-audio-generation': 'Audio generation',
        'cap-header-system': 'System abilities',
        'cap-web-search': 'Web search / browsing',
        'cap-document': 'Document & PDF understanding',
        'cap-file-handling': 'File handling',
        'cap-api': 'API calling',
        'cap-computer-use': 'Computer use',
        'cap-header-automation': 'Automation',
        'cap-agents': 'Agents / autonomous actions',
        'cap-workflows': 'Multi-step workflows',
        'cap-scheduling': 'Scheduling',
        'cap-tool-use': 'Tool use',
        'about-title': 'Om AI Score',
        'about-intro': 'Et eksperiment fra FYRK Lab hvor vi utforsker hvordan man kan sammenligne AI-modeller på en enkel måte.',
        'about-sources-title': 'Datakilder',
        'source-1': 'Offentlig tilgjengelig informasjon',
        'source-2': 'Egne praktiske tester',
        'source-3': 'Inntrykk fra utviklere og AI-miljøer',
        'source-4': 'Vurderinger generert og validert med AI',
        'disclaimer': 'Ikke vitenskapelig – bruk som inspirasjon, ikke fasit.'
    },
    sv: {
        'hero-badge': 'Uppdaterad desember 2025',
        'hero-subtitle': 'Månadsvis rangering av AI-verktyg baserat på buzz, sentiment och nytta',
        'new-this-month': 'Nytt denna månad',
        'biggest-changes': 'Största förändringarna',
        'metrics-title': 'Så här läser du datan',
        'metric-buzz': 'Hur mycket modellen/verktyget diskuteras (0–100)',
        'metric-sentiment': 'Hur positivt/negativt det omtalas i communityt',
        'metric-utility': 'Upplevd praktisk nytta',
        'metric-price': 'Upplevd kostnad/nytta (lägre = bättre värde)',
        'label-utility': 'Nytta',
        'label-price': 'Pris',
        'filter-label': 'Filtrera efter kategori:',
        'filter-all': 'Alla',
        'cat-core-llm': 'Kärn-LLM:er',
        'cat-code': 'Kodassistenter',
        'cat-image': 'Bild & Video',
        'cat-audio': 'Ljud & Röst',
        'cat-agents': 'Agenter & Automatisering',
        'models': 'modeller',
        'tools': 'verktyg',
        'platforms': 'plattformar',
        'cta-title': 'Vill du använda AI mer effektivt i ditt team?',
        'cta-text': 'FYRK hjälper företag att välja rätt verktyg och bygga AI-drivna arbetsflöden.',
        'cta-button': 'Kontakta oss',
        'contact': 'Kontakt',
        'last-updated': 'Senast uppdaterad: 4. des 2025',
        'show-all': 'Visa alla',
        'show-fewer': 'Visa färre',
        'tab-scores': 'Rankings',
        'tab-capabilities': 'Model Abilities',
        'lab-badge': '🧪 FYRK Lab',
        'lab-text': 'Ett experiment – inte en benchmark.',
        'les-mer': 'Läs mer',
        'close': 'Stäng',
        'capabilities-title': 'Kapabiliteter',
        'capabilities-subtitle': 'Vad kan varje modell?',
        'legend-best': 'Bäst',
        'legend-yes': 'Ja',
        'legend-partial': 'Delvis',
        'legend-no': 'Nej',
        'cap-header-cognitive': 'Cognitive abilities',
        'cap-reasoning': 'Reasoning',
        'cap-coding': 'Coding',
        'cap-memory': 'Memory (context)',
        'cap-multilingual': 'Multilingual / Norwegian',
        'cap-header-visual': 'Visual abilities',
        'cap-image-gen': 'Image generation',
        'cap-image-understanding': 'Image understanding',
        'cap-video-gen': 'Video generation',
        'cap-video-understanding': 'Video understanding',
        'cap-header-audio': 'Audio & speech',
        'cap-speech-to-text': 'Speech-to-text',
        'cap-text-to-speech': 'Text-to-speech',
        'cap-audio-understanding': 'Audio understanding',
        'cap-audio-generation': 'Audio generation',
        'cap-header-system': 'System abilities',
        'cap-web-search': 'Web search / browsing',
        'cap-document': 'Document & PDF understanding',
        'cap-file-handling': 'File handling',
        'cap-api': 'API calling',
        'cap-computer-use': 'Computer use',
        'cap-header-automation': 'Automation',
        'cap-agents': 'Agents / autonomous actions',
        'cap-workflows': 'Multi-step workflows',
        'cap-scheduling': 'Scheduling',
        'cap-tool-use': 'Tool use',
        'about-title': 'Om AI Score',
        'about-intro': 'Ett experiment från FYRK Lab där vi utforskar hur man kan jämföra AI-modeller på ett enkelt sätt.',
        'about-sources-title': 'Datakällor',
        'source-1': 'Offentligt tillgänglig information',
        'source-2': 'Egna praktiska tester',
        'source-3': 'Intryck från utvecklare och AI-miljöer',
        'source-4': 'Bedömningar genererade och validerade med AI',
        'disclaimer': 'Inte vetenskapligt – använd som inspiration, inte facit.'
    },
    en: {
        'hero-badge': 'Updated desember 2025',
        'hero-subtitle': 'Monthly ranking of AI tools based on buzz, sentiment, and utility',
        'new-this-month': 'New This Month',
        'biggest-changes': 'Biggest Movers',
        'metrics-title': 'How to Read the Data',
        'metric-buzz': 'How much the model/tool is being discussed (0–100)',
        'metric-sentiment': 'How positively/negatively it\'s talked about in the community',
        'metric-utility': 'Perceived practical usefulness',
        'metric-price': 'Perceived cost/value (lower = better value)',
        'label-utility': 'Utility',
        'label-price': 'Price',
        'filter-label': 'Filter by category:',
        'filter-all': 'All',
        'cat-core-llm': 'Core LLMs',
        'cat-code': 'Code Assistants',
        'cat-image': 'Image & Video',
        'cat-audio': 'Audio & Voice',
        'cat-agents': 'Agents & Automation',
        'models': 'models',
        'tools': 'tools',
        'platforms': 'platforms',
        'cta-title': 'Want to use AI more effectively in your team?',
        'cta-text': 'FYRK helps companies choose the right tools and build AI-powered workflows.',
        'cta-button': 'Contact Us',
        'contact': 'Contact',
        'last-updated': 'Last updated: 4. des 2025',
        'show-all': 'Show all',
        'show-fewer': 'Show fewer',
        'tab-scores': 'Scores',
        'tab-capabilities': 'Capabilities',
        'lab-badge': '🧪 FYRK Lab',
        'lab-text': 'An experiment – not a benchmark.',
        'les-mer': 'Read more',
        'close': 'Close',
        'capabilities-title': 'Capabilities',
        'capabilities-subtitle': 'What can each model do?',
        'legend-best': 'Best',
        'legend-yes': 'Yes',
        'legend-partial': 'Partial',
        'legend-no': 'No',
        'cap-header-cognitive': 'Cognitive abilities',
        'cap-reasoning': 'Reasoning',
        'cap-coding': 'Coding',
        'cap-memory': 'Memory (context)',
        'cap-multilingual': 'Multilingual / Norwegian',
        'cap-header-visual': 'Visual abilities',
        'cap-image-gen': 'Image generation',
        'cap-image-understanding': 'Image understanding',
        'cap-video-gen': 'Video generation',
        'cap-video-understanding': 'Video understanding',
        'cap-header-audio': 'Audio & speech',
        'cap-speech-to-text': 'Speech-to-text',
        'cap-text-to-speech': 'Text-to-speech',
        'cap-audio-understanding': 'Audio understanding',
        'cap-audio-generation': 'Audio generation',
        'cap-header-system': 'System abilities',
        'cap-web-search': 'Web search / browsing',
        'cap-document': 'Document & PDF understanding',
        'cap-file-handling': 'File handling',
        'cap-api': 'API calling',
        'cap-computer-use': 'Computer use',
        'cap-header-automation': 'Automation',
        'cap-agents': 'Agents / autonomous actions',
        'cap-workflows': 'Multi-step workflows',
        'cap-scheduling': 'Scheduling',
        'cap-tool-use': 'Tool use',
        'about-title': 'About AI Score',
        'about-intro': 'An experiment from FYRK Lab exploring how to compare AI models in a simple way.',
        'about-sources-title': 'Data Sources',
        'source-1': 'Publicly available information',
        'source-2': 'Own practical tests',
        'source-3': 'Impressions from developers and AI communities',
        'source-4': 'Assessments generated and validated with AI',
        'disclaimer': 'Not scientific – use as inspiration, not fact.'
    }
};

let currentLang = localStorage.getItem('fyrk-lang') || 'no';

function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('fyrk-lang', lang);
    
    // Update active button
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });
    
    // Translate all elements
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        if (translations[lang] && translations[lang][key]) {
            el.textContent = translations[lang][key];
        }
    });
    
    // Translate expand buttons based on their expanded state
    document.querySelectorAll('.expand-toggle, .expand-button').forEach(button => {
        const expandText = button.querySelector('.expand-text');
        if (expandText) {
            const isExpanded = button.classList.contains('expanded');
            const key = isExpanded ? 'show-fewer' : 'show-all';
            if (translations[lang] && translations[lang][key]) {
                expandText.textContent = translations[lang][key];
            }
        }
    });
    
    // Re-render capabilities to update translations
    renderCapabilitiesTable();
    renderCapabilitiesMobile();
    
    // Update html lang attribute
    document.documentElement.lang = lang === 'no' ? 'no' : lang === 'sv' ? 'sv' : 'en';
}

// Lab Banner Dismissal
function dismissLabBanner() {
    const banner = document.getElementById('lab-banner');
    if (banner) {
        banner.classList.add('hidden');
        localStorage.setItem('fyrk-lab-banner-dismissed', 'true');
    }
}

// Tab Navigation
function switchTab(tabName) {
    // Update tabs
    document.querySelectorAll('.tab').forEach(tab => {
        const isActive = tab.dataset.tab === tabName;
        tab.classList.toggle('active', isActive);
        tab.setAttribute('aria-selected', isActive);
    });

    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        const isActive = content.id === 'tab-' + tabName;
        content.classList.toggle('hidden', !isActive);
        content.setAttribute('aria-hidden', !isActive);
    });

    // Update URL hash
    window.location.hash = tabName;

    // Store in localStorage
    localStorage.setItem('fyrk-active-tab', tabName);
}

// Capabilities Configuration
const CAPABILITIES_CONFIG = {
    tools: ['Claude Opus 4.5', 'ChatGPT (GPT-5)', 'Gemini (2.5/3 Pro)', 'Grok 3/4', 'Llama 4', 'DeepSeek (V3/R1)'],
    providerNames: {
        'Claude Opus 4.5': 'Anthropic',
        'ChatGPT (GPT-5)': 'OpenAI',
        'Gemini (2.5/3 Pro)': 'Google',
        'Grok 3/4': 'xAI',
        'Llama 4': 'Meta',
        'DeepSeek (V3/R1)': 'DeepSeek'
    },
    scoreSymbols: {
        'best': '⭐',
        'yes': '✔︎',
        'no': '✗',
        'partial': '~'
    },
    categories: [
        { type: 'header', key: 'cap-header-cognitive' },
        { key: 'cap-reasoning', shortKey: 'cap-reasoning', scores: ['yes', 'yes', 'best', 'yes', 'partial', 'yes'] },
        { key: 'cap-coding', shortKey: 'cap-coding', scores: ['best', 'yes', 'yes', 'yes', 'yes', 'yes'] },
        { key: 'cap-memory', shortKey: 'cap-memory', scores: ['yes', 'yes', 'yes', 'yes', 'best', 'yes'] },
        { type: 'header', key: 'cap-header-visual' },
        { key: 'cap-image-gen', shortKey: 'cap-image-gen', scores: ['no', 'yes', 'best', 'yes', 'no', 'no'] },
        { key: 'cap-image-understanding', shortKey: 'cap-image-understanding', scores: ['yes', 'yes', 'yes', 'yes', 'yes', 'partial'] },
        { key: 'cap-video-gen', shortKey: 'cap-video-gen', scores: ['no', 'yes', 'best', 'yes', 'no', 'no'] },
        { key: 'cap-video-understanding', shortKey: 'cap-video-understanding', scores: ['partial', 'yes', 'best', 'yes', 'yes', 'no'] },
        { type: 'header', key: 'cap-header-audio' },
        { key: 'cap-speech-to-text', shortKey: 'cap-speech-to-text', scores: ['no', 'yes', 'yes', 'yes', 'partial', 'no'] },
        { key: 'cap-text-to-speech', shortKey: 'cap-text-to-speech', scores: ['no', 'yes', 'yes', 'yes', 'partial', 'no'] },
        { key: 'cap-audio-understanding', shortKey: 'cap-audio-understanding', scores: ['no', 'yes', 'yes', 'partial', 'partial', 'no'] },
        { key: 'cap-audio-generation', shortKey: 'cap-audio-generation', scores: ['no', 'yes', 'yes', 'partial', 'no', 'no'] },
        { type: 'header', key: 'cap-header-system' },
        { key: 'cap-web-search', shortKey: 'cap-web-search', scores: ['yes', 'yes', 'yes', 'yes', 'partial', 'yes'] },
        { key: 'cap-document', shortKey: 'cap-document', scores: ['yes', 'yes', 'yes', 'yes', 'yes', 'yes'] },
        { key: 'cap-file-handling', shortKey: 'cap-file-handling', scores: ['yes', 'yes', 'yes', 'partial', 'partial', 'partial'] },
        { key: 'cap-api', shortKey: 'cap-api', scores: ['yes', 'yes', 'yes', 'yes', 'yes', 'yes'] },
        { key: 'cap-computer-use', shortKey: 'cap-computer-use', scores: ['best', 'partial', 'yes', 'no', 'no', 'no'] },
        { type: 'header', key: 'cap-header-automation' },
        { key: 'cap-agents', shortKey: 'cap-agents', scores: ['best', 'yes', 'yes', 'partial', 'partial', 'partial'] },
        { key: 'cap-workflows', shortKey: 'cap-workflows', scores: ['yes', 'yes', 'yes', 'yes', 'partial', 'yes'] },
        { key: 'cap-scheduling', shortKey: 'cap-scheduling', scores: ['partial', 'partial', 'partial', 'no', 'no', 'no'] },
        { key: 'cap-tool-use', shortKey: 'cap-tool-use', scores: ['best', 'yes', 'yes', 'yes', 'yes', 'yes'] },
    ]
};

// Capabilities Utilities
const CapabilitiesUtils = {
    getTranslation: (key) => {
        return translations[currentLang] && translations[currentLang][key] || key;
    },
    
    getCapabilityName: (category) => {
        const nameKey = category.shortKey || category.key;
        return CapabilitiesUtils.getTranslation(nameKey);
    },
    
    createScoreCell: (score) => {
        const cell = document.createElement('td');
        const cellContent = document.createElement('div');
        cellContent.className = `capability-cell capability-${score}`;
        const symbol = CAPABILITIES_CONFIG.scoreSymbols[score] || '';
        cellContent.textContent = symbol;
        cell.appendChild(cellContent);
        return cell;
    },
    
    createCategoryHeader: (category) => {
        const row = document.createElement('tr');
        row.className = 'category-header';
        const headerCell = document.createElement('td');
        headerCell.setAttribute('data-i18n', category.key);
        headerCell.setAttribute('colspan', CAPABILITIES_CONFIG.tools.length + 1);
        headerCell.textContent = CapabilitiesUtils.getTranslation(category.key);
        row.appendChild(headerCell);
        return row;
    },
    
    createCapabilityRow: (category) => {
        const row = document.createElement('tr');
        const nameCell = document.createElement('td');
        const nameKey = category.shortKey || category.key;
        nameCell.setAttribute('data-i18n', nameKey);
        nameCell.textContent = CapabilitiesUtils.getCapabilityName(category);
        row.appendChild(nameCell);
        
        category.scores.forEach(score => {
            row.appendChild(CapabilitiesUtils.createScoreCell(score));
        });
        
        return row;
    }
};

// Render Capabilities Table
function renderCapabilitiesTable() {
    const tbody = document.getElementById('capabilities-tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    CAPABILITIES_CONFIG.categories.forEach(category => {
        if (category.type === 'header') {
            tbody.appendChild(CapabilitiesUtils.createCategoryHeader(category));
        } else {
            tbody.appendChild(CapabilitiesUtils.createCapabilityRow(category));
        }
    });
}

function renderCapabilitiesMobile() {
    // Mobile view can be implemented later if needed
}

// Expand/collapse functionality - defined globally
function toggleExpand(categoryId) {
    try {
        // Find button by data-category attribute
        const button = document.querySelector('.expand-button[data-category="' + categoryId + '"]');
        if (!button) {
            console.error('Expand button not found for category:', categoryId);
            return;
        }
        
        // Find the table container (parent of expand-section)
        const expandSection = button.closest('.expand-section');
        if (!expandSection) {
            console.error('Expand section not found');
            return;
        }
        
        const table = expandSection.parentElement;
        if (!table || !table.classList.contains('rankings-table')) {
            console.error('Table not found');
            return;
        }
        
        const hiddenRows = table.querySelectorAll('.ranking-row.hidden-row');
        const expandText = button.querySelector('.expand-text');
        
        if (button.classList.contains('expanded')) {
            // Collapse
            hiddenRows.forEach(row => {
                row.classList.remove('expanded');
            });
            button.classList.remove('expanded');
            if (expandText) {
                // Use translation - button is now collapsed, so show "show-all"
                const key = 'show-all';
                const lang = localStorage.getItem('fyrk-lang') || 'no';
                if (translations[lang] && translations[lang][key]) {
                    expandText.textContent = translations[lang][key];
                } else {
                    expandText.textContent = 'Vis alle';
                }
            }
        } else {
            // Expand
            hiddenRows.forEach(row => {
                row.classList.add('expanded');
            });
            button.classList.add('expanded');
            if (expandText) {
                // Use translation - button is now expanded, so show "show-fewer"
                const key = 'show-fewer';
                const lang = localStorage.getItem('fyrk-lang') || 'no';
                if (translations[lang] && translations[lang][key]) {
                    expandText.textContent = translations[lang][key];
                } else {
                    expandText.textContent = 'Vis færre';
                }
            }
        }
    } catch (error) {
        console.error('Error in toggleExpand:', error);
    }
}

// Make function available globally
window.toggleExpand = toggleExpand;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize language
    setLanguage(currentLang);
    
    // Language switcher
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => setLanguage(btn.dataset.lang));
    });

    // Initialize tabs
    const hash = window.location.hash.slice(1);
    const savedTab = localStorage.getItem('fyrk-active-tab');
    const defaultTab = hash || savedTab || 'scores';
    switchTab(defaultTab);

    // Tab click handlers
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });

    // Handle browser back/forward
    window.addEventListener('hashchange', function() {
        const hash = window.location.hash.slice(1);
        if (hash === 'scores' || hash === 'kapabiliteter') {
            switchTab(hash);
        }
    });

    // Check if lab banner was dismissed
    if (localStorage.getItem('fyrk-lab-banner-dismissed') === 'true') {
        const banner = document.getElementById('lab-banner');
        if (banner) banner.classList.add('hidden');
    }

    // Render capabilities
    renderCapabilitiesTable();
    renderCapabilitiesMobile();

    // Category filtering
    const filterPills = document.querySelectorAll('.filter-pill');
    const categorySections = document.querySelectorAll('.category-section');

    filterPills.forEach(pill => {
        pill.addEventListener('click', function() {
            const category = this.dataset.category;
            
            // Update active state
            filterPills.forEach(p => p.classList.remove('active'));
            this.classList.add('active');
            
            // Show/hide categories
            categorySections.forEach(section => {
                if (category === 'all' || section.dataset.category === category) {
                    section.classList.remove('hidden');
                } else {
                    section.classList.add('hidden');
                }
            });
        });
    });

    // Column sorting
    document.querySelectorAll('.rankings-header span[data-sort]').forEach(header => {
        header.addEventListener('click', function() {
            const sortKey = this.dataset.sort;
            const table = this.closest('.rankings-table');
            const expandSection = table.querySelector('.expand-section');
            const rows = Array.from(table.querySelectorAll('.ranking-row'));
            const isAsc = this.classList.contains('sort-asc');
            
            // Reset all sort indicators in this table
            table.querySelectorAll('.rankings-header span[data-sort]').forEach(h => {
                h.classList.remove('sort-asc', 'sort-desc');
            });
            
            // Set new sort direction
            this.classList.add(isAsc ? 'sort-desc' : 'sort-asc');
            
            // Sort rows
            rows.sort((a, b) => {
                let valA, valB;
                
                if (sortKey === 'name') {
                    valA = a.querySelector('.item-name').textContent.toLowerCase();
                    valB = b.querySelector('.item-name').textContent.toLowerCase();
                    return isAsc ? valB.localeCompare(valA) : valA.localeCompare(valB);
                } else {
                    valA = parseInt(a.dataset[sortKey]) || 0;
                    valB = parseInt(b.dataset[sortKey]) || 0;
                    return isAsc ? valA - valB : valB - valA;
                }
            });
            
            // Re-append rows and update rank badges
            rows.forEach((row, index) => {
                if (expandSection) {
                    table.insertBefore(row, expandSection);
                } else {
                    table.appendChild(row);
                }
                const badge = row.querySelector('.rank-badge');
                badge.textContent = index + 1;
                badge.className = 'rank-badge';
                if (index === 0) badge.classList.add('rank-1');
                else if (index === 1) badge.classList.add('rank-2');
                else if (index === 2) badge.classList.add('rank-3');
                else badge.classList.add('rank-default');
            });
        });
    });
});
