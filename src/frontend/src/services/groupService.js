import apiClient from '../api/client';

export const getGroups = async () => {
  try {
    const response = await apiClient.get('/groups');
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to fetch groups',
    };
  }
};

export const getGroup = async (id) => {
  try {
    const response = await apiClient.get(`/groups/${id}`);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to fetch group',
    };
  }
};

export const createGroup = async (groupData) => {
  try {
    const response = await apiClient.post('/groups', groupData);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to create group',
    };
  }
};

export const updateGroup = async (id, groupData) => {
  try {
    const response = await apiClient.put(`/groups/${id}`, groupData);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to update group',
    };
  }
};

export const deleteGroup = async (id) => {
  try {
    await apiClient.delete(`/groups/${id}`);
    return { success: true };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to delete group',
    };
  }
};

export const clusterizeNotes = async () => {
  try {
    const response = await apiClient.post('/groups/clusterize');
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to clusterize notes',
    };
  }
};

