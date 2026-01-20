import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import * as groupService from '../services/groupService';
import GroupCard from './GroupCard';

const GroupList = () => {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [clustering, setClustering] = useState(false);
  const navigate = useNavigate();

  const fetchGroups = async () => {
    setLoading(true);
    setError('');
    const result = await groupService.getGroups();
    setLoading(false);

    if (result.success) {
      setGroups(result.data);
    } else {
      setError(result.error || 'Failed to load groups');
    }
  };

  const handleClusterize = async () => {
    setClustering(true);
    setError('');
    const result = await groupService.clusterizeNotes();
    setClustering(false);

    if (result.success) {
      // Reload groups after clustering
      await fetchGroups();
    } else {
      setError(result.error || 'Failed to clusterize notes');
    }
  };

  useEffect(() => {
    fetchGroups();
  }, []);

  if (loading) {
    return <div className="loading">Loading groups...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="note-list">
      <div className="note-list-header">
        <h1>My Groups</h1>
        <button 
          className="btn btn-primary" 
          onClick={handleClusterize}
          disabled={clustering}
        >
          {clustering ? 'Clustering...' : 'Group Notes'}
        </button>
      </div>
      {groups.length === 0 ? (
        <div className="empty-state">
          <p>No groups yet. Click "Group Notes" to cluster your notes into groups.</p>
        </div>
      ) : (
        <div className="note-grid">
          {groups.map((group) => (
            <GroupCard key={group.id} group={group} onDelete={fetchGroups} />
          ))}
        </div>
      )}
    </div>
  );
};

export default GroupList;

