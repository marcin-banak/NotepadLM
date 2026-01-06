import apiClient from '../api/client';

export const getNotes = async () => {
  try {
    const response = await apiClient.get('/notes');
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to fetch notes',
    };
  }
};

export const getNote = async (id) => {
  try {
    const response = await apiClient.get(`/notes/${id}`);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to fetch note',
    };
  }
};

export const createNote = async (noteData) => {
  try {
    const response = await apiClient.post('/notes', noteData);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to create note',
    };
  }
};

export const updateNote = async (id, noteData) => {
  try {
    const response = await apiClient.put(`/notes/${id}`, noteData);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to update note',
    };
  }
};

export const deleteNote = async (id) => {
  try {
    await apiClient.delete(`/notes/${id}`);
    return { success: true };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to delete note',
    };
  }
};

