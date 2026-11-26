// API Client for Abusive-Language Screening Academic Platform
const API = {
  baseUrl: '',

  async pullGist() {
    const res = await fetch(`${this.baseUrl}/api/briefs/digest`);
    return res.json();
  },

  async scan(payload) {
    const res = await fetch(`${this.baseUrl}/api/scan/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Detection failed');
    }
    return res.json();
  },

  async extractGlyphs(payload) {
    const res = await fetch(`${this.baseUrl}/api/scan/read-glyphs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'OCR extraction failed');
    }
    return res.json();
  },

  async sendReview(payload) {
    const res = await fetch(`${this.baseUrl}/api/reviews/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Feedback submission failed');
    }
    return res.json();
  },

  async pullReviewRoll() {
    const res = await fetch(`${this.baseUrl}/api/reviews/`);
    return res.json();
  },

  async pullCorpora() {
    const res = await fetch(`${this.baseUrl}/api/corpora/`);
    return res.json();
  },

  async enrollCorpus(payload) {
    const res = await fetch(`${this.baseUrl}/api/corpora/enroll`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Registration failed');
    }
    return res.json();
  },

  async examineCorpus(datasetId, params = {}) {
    const q = new URLSearchParams();
    if (params.limit != null) q.append('limit', params.limit);
    if (params.offset != null) q.append('offset', params.offset);
    if (params.label_filter != null) q.append('label_filter', params.label_filter);
    if (params.search != null) q.append('search', params.search);
    const qs = q.toString() ? `?${q.toString()}` : '';
    const res = await fetch(`${this.baseUrl}/api/corpora/${datasetId}/examine${qs}`);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Inspection failed');
    }
    return res.json();
  },

  async pullEngines() {
    const res = await fetch(`${this.baseUrl}/api/engines/`);
    return res.json();
  },

  async chooserEngine(modelId) {
    const res = await fetch(`${this.baseUrl}/api/engines/activate/${modelId}`, { method: 'POST' });
    return res.json();
  },

  async fireTuning(payload) {
    const res = await fetch(`${this.baseUrl}/api/tuning/launch`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Optimization failed');
    }
    return res.json();
  },

  async pullTuningLog() {
    const res = await fetch(`${this.baseUrl}/api/tuning/log`);
    return res.json();
  },

  async simulatePayoff(payload) {
    const res = await fetch(`${this.baseUrl}/api/tuning/preview-score`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Reward simulation failed');
    }
    return res.json();
  },

  async pullEquityProbe() {
    const res = await fetch(`${this.baseUrl}/api/equity/review`);
    return res.json();
  },

  async fireEquityPoke(payload) {
    const res = await fetch(`${this.baseUrl}/api/equity/what-if`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Fairness probe failed');
    }
    return res.json();
  },

  async pullTrials() {
    const res = await fetch(`${this.baseUrl}/api/trials/`);
    return res.json();
  },

  async fireTrial(expCode) {
    const res = await fetch(`${this.baseUrl}/api/trials/execute/${expCode}`, { method: 'POST' });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Experiment execution failed');
    }
    return res.json();
  },

  async fireEveryTrials() {
    const res = await fetch(`${this.baseUrl}/api/trials/run-suite`, { method: 'POST' });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Batch experiment execution failed');
    }
    return res.json();
  },

  async rewindTrials() {
    const res = await fetch(`${this.baseUrl}/api/trials/clear`, { method: 'POST' });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Reset failed');
    }
    return res.json();
  },

  async pullThesisSketch() {
    const res = await fetch(`${this.baseUrl}/api/briefs/manuscript`);
    return res.json();
  },

  async pullPrefs() {
    const res = await fetch(`${this.baseUrl}/api/preferences/`);
    return res.json();
  },

  async patchPrefs(payload) {
    const res = await fetch(`${this.baseUrl}/api/preferences/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  }
};

