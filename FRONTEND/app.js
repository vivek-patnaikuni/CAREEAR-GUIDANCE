/* FINAL WORKING APP.JS WITH SMOOTH SCROLL + REALISTIC REASONS */

document.addEventListener("DOMContentLoaded", () => {

  //SMOOTH SCROLL
  document.querySelectorAll("[data-scroll]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const sel = btn.getAttribute("data-scroll");
      const el = document.querySelector(sel);
      if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  //PDF Extraction 
  async function extractTextFromPDF(file) {
    try {
      const buffer = await file.arrayBuffer();
      const pdf = await pdfjsLib.getDocument({ data: buffer }).promise;
      let full = "";

      for (let p = 1; p <= pdf.numPages; p++) {
        const page = await pdf.getPage(p);
        const txt = await page.getTextContent();
        const strings = txt.items.map((i) => i.str);
        full += strings.join(" ") + "\n";
      }

      return full.trim();
    } catch (err) {
      console.error("PDF ERROR:", err);
      return "";
    }
  }

  const resumes = { domain: "", match: "", improve: "" };

  function getCheckedInterests() {
    return Array.from(
      document.querySelectorAll('#domain-section input[name="interest"]:checked')
    ).map((x) => x.value);
  }

  function showOverlay(text) {
    const o = document.getElementById("overlayMsg");
    const t = document.getElementById("overlayText");
    t.textContent = text;
    o.classList.remove("hidden");
  }

  document.getElementById("overlayOk").addEventListener("click", () => {
    document.getElementById("overlayMsg").classList.add("hidden");
  });

  //FILE INPUT HANDLERS
  function setupFileInput(inputId, nameId, storeKey) {
    const input = document.getElementById(inputId);
    const label = document.getElementById(nameId);

    input.addEventListener("change", async (e) => {
      const f = e.target.files[0];
      label.textContent = f ? f.name : "No file chosen";

      if (f && f.type === "application/pdf") {
        label.textContent = "Extracting...";
        resumes[storeKey] = await extractTextFromPDF(f);
        label.textContent = f.name;
      }
    });
  }

  setupFileInput("file-input-domain", "file-name-domain", "domain");
  setupFileInput("file-input-match", "file-name-match", "match");
  setupFileInput("file-input-improve", "file-name-improve", "improve");

  // DOMAIN DESCRIPTION (STATIC TEXT)  

  function generateDomainDescription(domain) {
    switch (domain) {
      case "Artificial Intelligence":
        return "Artificial Intelligence focuses on building intelligent systems that learn from data using machine learning and deep learning.";

      case "Web Development":
        return "Web Development involves designing, building, and deploying interactive websites using frontend and backend technologies.";

      case "Cloud Computing":
        return "Cloud Computing deals with deploying, scaling, and managing applications on cloud platforms such as AWS, Azure, and Google Cloud.";

      case "Cyber Security":
        return "Cyber Security focuses on protecting systems, networks, and sensitive data from cyber attacks and vulnerabilities.";

      case "Data Analyst":
        return "Data Analytics focuses on extracting insights from data using tools like Python, SQL, Excel, and visualization software.";

      case "Mobile App Development":
        return "Mobile App Development focuses on building applications for Android and iOS using frameworks such as Flutter, Java, or React Native.";

      default:
        return "This domain matches your resume keywords and selected interests.";
    }
  }

 //GET DOMAIN 

  document.getElementById("getDomainBtn").addEventListener("click", async () => {
    const file = document.getElementById("file-input-domain").files[0];
    const interests = getCheckedInterests();

    if (!file && interests.length === 0)
      return showOverlay("PLEASE SELECT INTERESTS AND UPLOAD YOUR RESUME");

    if (!file)
      return showOverlay("PLEASE UPLOAD YOUR RESUME");

    if (interests.length === 0)
      return showOverlay("PLEASE SELECT YOUR INTERESTS");

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("interests", interests.join(","));

    const res = await fetch("http://localhost:5000/recommend_domain", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    const description = generateDomainDescription(data.domain);

    /* Save domain + real matched skills + real interests */
    localStorage.setItem(
      "cg_result",
      JSON.stringify({
        type: "domain",
        domain: data.domain,
        reason: description,
        skill_keywords: data.skill_keywords,
        interests_list: data.interests_list
      })
    );

    window.location.href = "domain_result.html";
  });

// SKILL MATCH 

document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const file = document.getElementById("file-input-match").files[0];
  const domainCode = document.getElementById("domainSelect").value;

  if (!file) return showOverlay("PLEASE UPLOAD YOUR RESUME");

  // SHORT CODE → FULL NAME FIX 🔥
  const domainMapFull = {
    AI: "Artificial Intelligence",
    Web: "Web Development",
    Cloud: "Cloud Computing",
    Cyber: "Cyber Security",
    Data: "Data Analyst",
    Mobile: "Mobile App Development",
  };

  const fullDomain = domainMapFull[domainCode];  // <— FIX

  const formData = new FormData();
  formData.append("resume", file);
  formData.append("domain", fullDomain);

  try {
    const res = await fetch("http://localhost:5000/skill_match", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    localStorage.setItem(
      "cg_result",
      JSON.stringify({
        type: "match",
        percent: data.percent,
        strengths: data.strengths,
        focus: data.focus,
      })
    );

    window.location.href = "match_result.html";

  } catch (err) {
    console.error(err);
    showOverlay("SERVER ERROR — CHECK BACKEND");
  }
});


  //RESUME IMPROVEMENT 

  document.getElementById("improveBtn").addEventListener("click", async () => {
    const file = document.getElementById("file-input-improve").files[0];

    if (!file) return showOverlay("PLEASE UPLOAD YOUR RESUME");

    const formData = new FormData();
    formData.append("resume", file);

    const res = await fetch("http://localhost:5000/improve_resume", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    localStorage.setItem(
      "cg_result",
      JSON.stringify({
        type: "improve",
        suggestions: data.suggestions,
      })
    );

    window.location.href = "improve_result.html";
  });

});
