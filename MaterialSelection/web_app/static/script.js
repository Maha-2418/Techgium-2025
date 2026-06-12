const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const recTemplate = document.getElementById('recommendation-template');
const themeToggle = document.getElementById('theme-toggle');

// Theme Logic
const savedTheme = localStorage.getItem('theme') || 'dark';
document.documentElement.setAttribute('data-theme', savedTheme);
updateThemeIcon(savedTheme);

themeToggle.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
});

function updateThemeIcon(theme) {
    if (theme === 'light') {
        themeToggle.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>`;
    } else {
        themeToggle.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`;
    }
}

function addMessage(text, type) {
    const div = document.createElement('div');
    div.className = `message ${type}`;
    div.textContent = text;
    chatContainer.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Update requirement from dropdown
window.updateRequirement = (baseTerm, level) => {
    let current = userInput.value;
    let terms = current.split(',').map(s => s.trim()).filter(s => s.length > 0);

    // Remove existing entry for this property
    // Matches "High Tensile Strength", "Low Tensile Strength", "Medium Tensile Strength"
    const regex = new RegExp(`^(High|Medium|Low) ${baseTerm}$`, 'i');
    terms = terms.filter(t => !regex.test(t));

    // Add new if level is selected
    if (level) {
        terms.push(`${level} ${baseTerm}`);
    }

    userInput.value = terms.join(', ');
};

// Toggle for simple tags (Process)
window.setInput = (term) => {
    let current = userInput.value;
    let terms = current.split(',').map(s => s.trim()).filter(s => s.length > 0);
    const index = terms.findIndex(t => t.toLowerCase() === term.toLowerCase());
    if (index >= 0) terms.splice(index, 1);
    else terms.push(term);
    userInput.value = terms.join(', ');
    userInput.focus();
};

function addRecommendation(data) {
    const clone = recTemplate.content.cloneNode(true);
    const card = clone.querySelector('.result-card');

    // Populate Data
    const name = data.recommended_material.name;
    const score = data.recommended_material.score;
    card.querySelector('.material-name').innerHTML = `${name} <span style="font-size: 0.8em; opacity: 0.8; margin-left: 10px;">(Score: ${score})</span>`;
    card.querySelector('.material-standard').textContent = data.recommended_material.standard;
    card.querySelector('.material-sustainability').textContent = data.recommended_material.sustainability_score;

    // Research Justification (Best Material)
    const researchSection = card.querySelector('.research-section');
    const researchContent = card.querySelector('.research-content');
    if (data.recommended_material.research_papers && data.recommended_material.research_papers.length > 0) {
        const rp = data.recommended_material.research_papers[0];
        researchSection.classList.remove('hidden');
        researchContent.innerHTML = `<strong>${rp.title}</strong><br><span style="opacity: 0.8; font-size: 0.9em;">Source: ${rp.reason}</span>`;
    }



    // Alternatives
    const altsContainer = card.querySelector('.alternatives-container');
    if (data.alternatives.length > 0) {
        data.alternatives.forEach(alt => {
            const altDiv = document.createElement('div');
            altDiv.className = 'alt-item';
            altDiv.style.marginBottom = '8px';

            const header = document.createElement('div');
            header.style.display = 'flex';
            header.style.justifyContent = 'space-between';
            header.style.alignItems = 'center';

            const title = document.createElement('span');
            title.innerHTML = `<strong>${alt.name}</strong> (Score: ${alt.score})`;

            const btn = document.createElement('button');
            btn.textContent = 'View Properties';
            // Use classes instead of inline styles for theme support
            btn.className = 'toggle-details alt-toggle-btn';

            header.appendChild(title);
            header.appendChild(btn);

            const details = document.createElement('div');
            details.className = 'properties-grid hidden';
            details.style.marginTop = '10px';
            details.style.borderTop = '1px solid #334155';
            details.style.paddingTop = '10px';

            // Populate alt props
            for (const [key, val] of Object.entries(alt.properties)) {
                if (typeof val !== 'object' && val !== null) {
                    const p = document.createElement('div');
                    p.className = 'prop-item';
                    p.textContent = `${key}: ${val}`;
                    details.appendChild(p);
                }
            }

            // Research Justification (Alternatives)
            if (alt.research_papers && alt.research_papers.length > 0) {
                const rp = alt.research_papers[0];
                const rs = document.createElement('div');
                rs.className = 'research-justification-card';
                rs.style.marginTop = '12px';
                rs.style.background = 'rgba(59, 130, 246, 0.05)';
                rs.style.padding = '10px';

                rs.innerHTML = `
                    <div class="research-header" style="font-size: 0.75rem; margin-bottom: 4px;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                        <span>Evidence</span>
                    </div>
                    <div class="research-content" style="font-size: 0.85rem;">
                        <strong>${rp.title}</strong><br>
                        <span style="opacity: 0.8;">Source: ${rp.reason}</span>
                    </div>
                `;
                details.appendChild(rs);
            }

            btn.addEventListener('click', () => {
                details.classList.toggle('hidden');
                btn.textContent = details.classList.contains('hidden') ? 'View Properties' : 'Hide';
            });

            altDiv.appendChild(header);
            altDiv.appendChild(details);
            altsContainer.appendChild(altDiv);
        });
    } else {
        card.querySelector('.alternatives-section').style.display = 'none';
    }

    // Applications
    const appList = card.querySelector('.applications-list');
    const apps = data.recommended_material.properties.applications || [];
    if (apps.length > 0) {
        apps.forEach(app => {
            const li = document.createElement('li');
            li.textContent = app;
            li.style.background = 'rgba(255,255,255,0.05)';
            li.style.padding = '4px 8px';
            li.style.borderRadius = '4px';
            li.style.display = 'inline-block';
            li.style.margin = '2px';
            li.style.fontSize = '0.85rem';
            appList.appendChild(li);
        });
    } else {
        card.querySelector('.applications-section').style.display = 'none';
    }



    // Details Toggle (Main)
    const toggleBtn = card.querySelector('.details-section .toggle-details');
    const propGrid = card.querySelector('.details-section .properties-grid');

    // Populate props
    const props = data.recommended_material.properties;
    for (const [key, val] of Object.entries(props)) {
        if (typeof val !== 'object' && val !== null) {
            const div = document.createElement('div');
            div.className = 'prop-item';
            div.textContent = `${key}: ${val}`;
            propGrid.appendChild(div);
        }
    }

    toggleBtn.addEventListener('click', () => {
        propGrid.classList.toggle('hidden');
        toggleBtn.textContent = propGrid.classList.contains('hidden') ? 'View Properties' : 'Hide Properties';
    });

    chatContainer.appendChild(card);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function handleSend() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    userInput.value = '';

    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: text })
        });

        if (!response.ok) {
            throw new Error(`Server returned status: ${response.status}`);
        }

        const data = await response.json();

        if (data.type === 'recommendation') {
            addRecommendation(data);
        } else if (data.type === 'clarification') {
            addMessage(data.message, 'system');
        } else if (data.type === 'error') {
            addMessage(`Error: ${data.message}`, 'system');
        } else {
            addMessage("Received unknown response format.", 'system');
        }

    } catch (err) {
        addMessage(`Failed to connect to server: ${err.message}`, 'system');
        console.error(err);
    }
}

sendBtn.addEventListener('click', handleSend);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend();
});
