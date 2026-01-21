import apiClient from '../api/client';

export const askQuestion = async (query, k = 10) => {
  try {
    const response = await apiClient.post('/ask', {
      query,
      k,
    });
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to ask question',
    };
  }
};

export const getAnswer = async (answerId) => {
  try {
    const response = await apiClient.get(`/ask/answer/${answerId}`);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to get answer',
    };
  }
};

export const getUserAnswers = async () => {
  try {
    const response = await apiClient.get('/ask/answers');
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to get answers',
    };
  }
};

export const deleteAnswer = async (answerId) => {
  try {
    await apiClient.delete(`/ask/answer/${answerId}`);
    return { success: true };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to delete answer',
    };
  }
};

export const convertAnswerToNote = async (answerId) => {
  try {
    const response = await apiClient.post(`/ask/answer/${answerId}/convert-to-note`);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to convert answer to note',
    };
  }
};

