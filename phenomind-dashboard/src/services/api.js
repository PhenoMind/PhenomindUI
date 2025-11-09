const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class ApiService {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    console.log(`[API] Making request to: ${url}`); // Debug log
    
    try {
      const response = await fetch(url, config);
      
      console.log(`[API] Response status: ${response.status}`); // Debug log
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error(`[API] Error response:`, errorText);
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log(`[API] Success:`, data); // Debug log
      return data;
    } catch (error) {
      console.error('[API] Request failed:', {
        url,
        error: error.message,
        type: error.name
      });
      
      // More specific error messages
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error(`Cannot connect to ${url}. Is the server running?`);
      }
      throw error;
    }
  }

  // Patient endpoints
  async getAllPatients(searchQuery = '') {
    const endpoint = searchQuery 
      ? `/api/patients?search=${encodeURIComponent(searchQuery)}`
      : '/api/patients';
    return this.request(endpoint);
  }

  async getPatientById(id) {
    return this.request(`/api/patients/${id}`);
  }

  async createPatient(patientData) {
    return this.request('/api/patients', {
      method: 'POST',
      body: JSON.stringify(patientData),
    });
  }

  async updatePatient(id, patientData) {
    return this.request(`/api/patients/${id}`, {
      method: 'PUT',
      body: JSON.stringify(patientData),
    });
  }

  async deletePatient(id) {
    return this.request(`/api/patients/${id}`, {
      method: 'DELETE',
    });
  }

  // Analytics endpoints
  async getPatientAnalytics(patientId) {
    return this.request(`/api/patients/${patientId}/analytics`);
  }

  async getPopulationAnalytics() {
    return this.request('/api/analytics/population');
  }

  async getRiskDistribution() {
    return this.request('/api/analytics/risk-distribution');
  }

  async getDisorderBreakdown() {
    return this.request('/api/analytics/disorder-breakdown');
  }
}

export default new ApiService();

