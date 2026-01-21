import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import * as groupService from '../services/groupService';
import GroupCard from './GroupCard';

const GroupList = () => {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [clustering, setClustering] = useState(false);
  const [viewMode, setViewMode] = useState('tiles'); // 'tiles' or 'list'
  const [selectedGroups, setSelectedGroups] = useState(new Set());
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

  const handleSelectGroup = (groupId) => {
    setSelectedGroups(prev => {
      const newSet = new Set(prev);
      if (newSet.has(groupId)) {
        newSet.delete(groupId);
      } else {
        newSet.add(groupId);
      }
      return newSet;
    });
  };

  const handleSelectAll = () => {
    if (selectedGroups.size === groups.length) {
      setSelectedGroups(new Set());
    } else {
      setSelectedGroups(new Set(groups.map(group => group.id)));
    }
  };

  const handleBulkDelete = async () => {
    if (selectedGroups.size === 0) return;
    
    if (window.confirm(`Are you sure you want to delete ${selectedGroups.size} group(s)?`)) {
      const deletePromises = Array.from(selectedGroups).map(groupId => 
        groupService.deleteGroup(groupId)
      );
      
      const results = await Promise.all(deletePromises);
      const failed = results.filter(r => !r.success);
      
      if (failed.length === 0) {
        setGroups(groups.filter(group => !selectedGroups.has(group.id)));
        setSelectedGroups(new Set());
      } else {
        alert(`Failed to delete ${failed.length} group(s)`);
        fetchGroups(); // Reload to sync state
      }
    }
  };

  const handleGroupClick = (groupId, e) => {
    // If clicking checkbox, don't navigate
    if (e.target.type === 'checkbox' || e.target.closest('.note-list-item-checkbox')) {
      return;
    }
    navigate(`/groups/${groupId}`);
  };

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
        <div className="note-list-header-actions">
          <div className="view-toggle">
            <button
              className={`view-toggle-btn ${viewMode === 'tiles' ? 'active' : ''}`}
              onClick={() => setViewMode('tiles')}
              title="Tile view"
            >
              <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <rect x="1" y="1" width="6" height="6" rx="1"/>
                <rect x="9" y="1" width="6" height="6" rx="1"/>
                <rect x="1" y="9" width="6" height="6" rx="1"/>
                <rect x="9" y="9" width="6" height="6" rx="1"/>
              </svg>
            </button>
            <button
              className={`view-toggle-btn ${viewMode === 'list' ? 'active' : ''}`}
              onClick={() => setViewMode('list')}
              title="List view"
            >
              <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <rect x="1" y="2" width="14" height="2" rx="0.5"/>
                <rect x="1" y="7" width="14" height="2" rx="0.5"/>
                <rect x="1" y="12" width="14" height="2" rx="0.5"/>
              </svg>
            </button>
          </div>
          <button 
            className="btn btn-primary" 
            onClick={handleClusterize}
            disabled={clustering}
          >
            {clustering ? 'Clustering...' : 'Group Notes'}
          </button>
        </div>
      </div>

      {selectedGroups.size > 0 && (
        <div className="selection-bar">
          <span className="selection-bar-text">
            {selectedGroups.size} {selectedGroups.size === 1 ? 'group' : 'groups'} selected
          </span>
          <button className="btn btn-secondary btn-small" onClick={handleSelectAll}>
            {selectedGroups.size === groups.length ? 'Deselect All' : 'Select All'}
          </button>
          <button className="btn btn-danger btn-small" onClick={handleBulkDelete}>
            Delete Selected
          </button>
        </div>
      )}

      {groups.length === 0 ? (
        <div className="empty-state">
          <p>No groups yet. Click "Group Notes" to cluster your notes into groups.</p>
        </div>
      ) : viewMode === 'tiles' ? (
        <div className="note-grid">
          {groups.map((group) => (
            <GroupCard
              key={group.id}
              group={group}
              onDelete={fetchGroups}
              isSelected={selectedGroups.has(group.id)}
              onSelect={() => handleSelectGroup(group.id)}
            />
          ))}
        </div>
      ) : (
        <div className="note-list-view">
          {groups.map((group) => (
            <div
              key={group.id}
              className={`note-list-item ${selectedGroups.has(group.id) ? 'selected' : ''}`}
              onClick={(e) => handleGroupClick(group.id, e)}
            >
              <input
                type="checkbox"
                className="note-list-item-checkbox"
                checked={selectedGroups.has(group.id)}
                onChange={() => handleSelectGroup(group.id)}
                onClick={(e) => e.stopPropagation()}
              />
              <span className="note-list-item-title">
                {group.summary || `Group ${group.id}`}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GroupList;

