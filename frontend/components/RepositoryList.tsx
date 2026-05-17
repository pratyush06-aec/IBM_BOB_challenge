"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FolderGit2, Trash2, Eye, Calendar, FileCode, Loader } from 'lucide-react';

interface Repository {
  id: string;
  name: string;
  description?: string;
  created_at: string;
  node_count: number;
  edge_count: number;
}

interface RepositoryListProps {
  token: string;
  onSelectRepository: (repoId: string) => void;
  refreshTrigger?: number;
}

const RepositoryList: React.FC<RepositoryListProps> = ({ 
  token, 
  onSelectRepository,
  refreshTrigger 
}) => {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const fetchRepositories = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/repository/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch repositories');
      }

      const data = await response.json();
      setRepositories(data);
      setError('');
    } catch (err: any) {
      setError(err.message || 'Failed to load repositories');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRepositories();
  }, [token, refreshTrigger]);

  const handleDelete = async (repoId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    
    if (!confirm('Are you sure you want to delete this repository?')) {
      return;
    }

    try {
      setDeletingId(repoId);
      const response = await fetch(`http://localhost:8000/api/repository/${repoId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to delete repository');
      }

      // Remove from list
      setRepositories(prev => prev.filter(repo => repo.id !== repoId));
    } catch (err: any) {
      alert(err.message || 'Failed to delete repository');
    } finally {
      setDeletingId(null);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader className="w-8 h-8 text-cyan-400 animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-500/20 border-2 border-red-500 rounded-xl">
        <p className="text-red-500 font-semibold">{error}</p>
      </div>
    );
  }

  if (repositories.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center py-12"
      >
        <FolderGit2 className="w-16 h-16 text-white/20 mx-auto mb-4" />
        <p className="text-white/60 text-lg">No repositories yet</p>
        <p className="text-white/40 text-sm mt-2">Upload your first repository to get started</p>
      </motion.div>
    );
  }

  return (
    <div className="space-y-4">
      <AnimatePresence>
        {repositories.map((repo, index) => (
          <motion.div
            key={repo.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ delay: index * 0.05 }}
            onClick={() => onSelectRepository(repo.id)}
            className="relative bg-white/5 backdrop-blur-xl border-2 border-white/10 rounded-2xl p-6 cursor-pointer hover:border-cyan-400 hover:bg-white/10 transition-all duration-300 group"
          >
            {/* Repository icon */}
            <div className="absolute top-6 right-6">
              <FolderGit2 className="w-8 h-8 text-cyan-400 group-hover:scale-110 transition-transform" />
            </div>

            {/* Repository info */}
            <div className="pr-16">
              <h3 className="text-xl font-black text-white mb-2 group-hover:text-cyan-400 transition-colors">
                {repo.name}
              </h3>
              
              {repo.description && (
                <p className="text-white/60 text-sm mb-4 line-clamp-2">
                  {repo.description}
                </p>
              )}

              {/* Stats */}
              <div className="flex items-center gap-6 text-sm">
                <div className="flex items-center gap-2">
                  <FileCode className="w-4 h-4 text-cyan-400" />
                  <span className="text-white/80">
                    {repo.node_count} nodes
                  </span>
                </div>
                
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4 text-cyan-400" />
                  <span className="text-white/80">
                    {formatDate(repo.created_at)}
                  </span>
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="absolute bottom-6 right-6 flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={(e) => {
                  e.stopPropagation();
                  onSelectRepository(repo.id);
                }}
                className="p-2 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 border-2 border-cyan-500"
              >
                <Eye className="w-4 h-4 text-cyan-400" />
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={(e) => handleDelete(repo.id, e)}
                disabled={deletingId === repo.id}
                className="p-2 rounded-lg bg-red-500/20 hover:bg-red-500/30 border-2 border-red-500 disabled:opacity-50"
              >
                {deletingId === repo.id ? (
                  <Loader className="w-4 h-4 text-red-400 animate-spin" />
                ) : (
                  <Trash2 className="w-4 h-4 text-red-400" />
                )}
              </motion.button>
            </div>

            {/* Hover effect */}
            <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-cyan-500/0 to-blue-500/0 group-hover:from-cyan-500/5 group-hover:to-blue-500/5 transition-all duration-300 pointer-events-none" />
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
};

export default RepositoryList;

// Made with Bob
