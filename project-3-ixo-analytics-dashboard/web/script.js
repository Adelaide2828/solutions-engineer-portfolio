// NumiKnow Facilitation Outcomes Dashboard Logic

const mockClaims = [
  {
    id: "CLM-NK-0184",
    school: "Hoedspruit Primary (Grade 6B)",
    facilitator: "did:ixo:entity:fac_thabo_01",
    scoreDelta: "38% → 72% (+34)",
    verdict: "approved",
    rule: "R1 (Cert Valid) + R2 (GPS Match 24m) + R3 (Photo Clear)",
    udid: "udid:ixo:rec_8f3a9e21...d4"
  },
  {
    id: "CLM-NK-0185",
    school: "Acornhoek Community School",
    facilitator: "did:ixo:entity:fac_sipho_09",
    scoreDelta: "45% → 78% (+33)",
    verdict: "approved",
    rule: "R1 (Cert Valid) + R2 (GPS Match 41m) + R3 (Photo Clear)",
    udid: "udid:ixo:rec_11b7a29c...89"
  },
  {
    id: "CLM-NK-0186",
    school: "Hoedspruit Primary (Grade 6A)",
    facilitator: "did:ixo:entity:fac_kelebogile_04",
    scoreDelta: "50% → 52% (+2)",
    verdict: "rejected",
    rule: "R2: GPS Mismatch (Claimed at -26.0, 28.0; >100m from school)",
    udid: "udid:ixo:rec_e41793aa...12"
  },
  {
    id: "CLM-NK-0187",
    school: "Mahlale Secondary Outreach",
    facilitator: "did:ixo:entity:fac_lerato_12",
    scoreDelta: "20% → 92% (+72)",
    verdict: "escalated",
    rule: "R4: Score Anomaly (>50pt jump flagged for SEF Auditor)",
    udid: "udid:ixo:rec_99214b7e...55"
  },
  {
    id: "CLM-NK-0188",
    school: "Bushbuckridge Education Hub",
    facilitator: "did:ixo:entity:fac_nomsa_07",
    scoreDelta: "40% → 68% (+28)",
    verdict: "rejected",
    rule: "R1: Invalid Facilitator Certificate (Score 74 < 80 threshold)",
    udid: "udid:ixo:rec_7c3a01ff...03"
  },
  {
    id: "CLM-NK-0189",
    school: "Hoedspruit Primary (Grade 6C)",
    facilitator: "did:ixo:entity:fac_thabo_01",
    scoreDelta: "35% → 70% (+35)",
    verdict: "escalated",
    rule: "R3: AI Image Confidence 0.62 (Classroom lighting blurry)",
    udid: "udid:ixo:rec_61a48c3d...22"
  },
  {
    id: "CLM-NK-0190",
    school: "Acornhoek Community School",
    facilitator: "did:ixo:entity:fac_tumelo_03",
    scoreDelta: "42% → 75% (+33)",
    verdict: "rejected",
    rule: "R5: Duplicate Hash Match (Same photo submitted 4 mins prior)",
    udid: "udid:ixo:rec_02df1488...a9"
  }
];

const mockFacilitators = [
  { name: "Thabo Mokoena", did: "did:ixo:entity:fac_thabo_01", sessions: 42, passRate: "95.2%", payout: "R 8,590.00", status: "Active" },
  { name: "Sipho Khumalo", did: "did:ixo:entity:fac_sipho_09", sessions: 38, passRate: "97.4%", payout: "R 7,955.00", status: "Active" },
  { name: "Lerato Dlamini", did: "did:ixo:entity:fac_lerato_12", sessions: 31, passRate: "87.1%", payout: "R 5,805.00", status: "Active" },
  { name: "Nomsa Sithole", did: "did:ixo:entity:fac_nomsa_07", sessions: 24, passRate: "79.2%", payout: "R 4,085.00", status: "Review" },
  { name: "Tumelo Phiri", did: "did:ixo:entity:fac_tumelo_03", sessions: 29, passRate: "89.6%", payout: "R 5,590.00", status: "Active" },
  { name: "Kelebogile Zulu", did: "did:ixo:entity:fac_kelebogile_04", sessions: 18, passRate: "83.3%", payout: "R 3,225.00", status: "Review" }
];

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  renderClaimsTable(mockClaims);
  renderFacilitatorsTable(mockFacilitators);
  initFilters();
  initCopyButton();
  initLiveClock();
  initSearch();
});

function initTabs() {
  const navItems = document.querySelectorAll(".nav-item");
  const tabPanes = document.querySelectorAll(".tab-pane");
  const tabTitle = document.getElementById("currentTabTitle");

  const titles = {
    overview: "Cohort Overview & Submissions",
    collection: "School Collection Deep-Dive",
    submitters: "Field Facilitators",
    evaluators: "SEF Auditors & Verifiers"
  };

  navItems.forEach(item => {
    item.addEventListener("click", () => {
      const targetTab = item.getAttribute("data-tab");

      navItems.forEach(nav => nav.classList.remove("active"));
      tabPanes.forEach(pane => pane.classList.remove("active"));

      item.classList.add("active");
      const activePane = document.getElementById(`tab-${targetTab}`);
      if (activePane) activePane.classList.add("active");

      if (tabTitle && titles[targetTab]) {
        tabTitle.textContent = titles[targetTab];
      }
    });
  });
}

function renderClaimsTable(claims) {
  const tbody = document.getElementById("claimsTableBody");
  if (!tbody) return;

  tbody.innerHTML = claims.map(claim => {
    let verdictBadge = "";
    if (claim.verdict === "approved") {
      verdictBadge = `<span class="badge-verdict verdict-approved">✓ Approved</span>`;
    } else if (claim.verdict === "rejected") {
      verdictBadge = `<span class="badge-verdict verdict-rejected">✕ Rejected</span>`;
    } else {
      verdictBadge = `<span class="badge-verdict verdict-escalated">⚠ Person Checks</span>`;
    }

    return `
      <tr>
        <td><strong>${claim.id}</strong></td>
        <td>${claim.school}</td>
        <td><code>${claim.facilitator}</code></td>
        <td><strong>${claim.scoreDelta}</strong></td>
        <td>${verdictBadge}</td>
        <td><small>${claim.rule}</small></td>
        <td><code>${claim.udid}</code></td>
      </tr>
    `;
  }).join("");
}

function renderFacilitatorsTable(facilitators) {
  const tbody = document.getElementById("facilitatorsTableBody");
  if (!tbody) return;

  tbody.innerHTML = facilitators.map(f => `
    <tr>
      <td><strong>${f.name}</strong></td>
      <td><code>${f.did}</code></td>
      <td>${f.sessions} sessions</td>
      <td><strong>${f.passRate}</strong></td>
      <td style="color: #10B981; font-weight: 600;">${f.payout}</td>
      <td><span class="pill-indicator" style="background: ${f.status === 'Active' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)'}; color: ${f.status === 'Active' ? '#10B981' : '#F59E0B'}">${f.status}</span></td>
    </tr>
  `).join("");
}

function initFilters() {
  const filterBtns = document.querySelectorAll(".filter-btn");
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      const filter = btn.getAttribute("data-filter");
      if (filter === "all") {
        renderClaimsTable(mockClaims);
      } else {
        const filtered = mockClaims.filter(c => c.verdict === filter);
        renderClaimsTable(filtered);
      }
    });
  });
}

function initCopyButton() {
  const copyBtn = document.getElementById("copyDidBtn");
  if (!copyBtn) return;

  copyBtn.addEventListener("click", () => {
    const did = "did:ixo:entity:8ebe9a34777a387dc04166cc1abe01ca";
    navigator.clipboard.writeText(did).then(() => {
      const originalHtml = copyBtn.innerHTML;
      copyBtn.innerHTML = `<code>Copied DID!</code>`;
      setTimeout(() => {
        copyBtn.innerHTML = originalHtml;
      }, 1800);
    });
  });
}

function initLiveClock() {
  const clockEl = document.getElementById("liveClock");
  if (!clockEl) return;

  setInterval(() => {
    const now = new Date();
    clockEl.textContent = now.toTimeString().split(" ")[0] + " Local";
  }, 1000);
}

function initSearch() {
  const searchInput = document.getElementById("facilitatorSearch");
  if (!searchInput) return;

  searchInput.addEventListener("input", (e) => {
    const query = e.target.value.toLowerCase();
    const filtered = mockFacilitators.filter(f => 
      f.name.toLowerCase().includes(query) || f.did.toLowerCase().includes(query)
    );
    renderFacilitatorsTable(filtered);
  });
}
