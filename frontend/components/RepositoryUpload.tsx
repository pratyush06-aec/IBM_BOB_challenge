"use client";

import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, X, File, CheckCircle, AlertCircle, Loader } from 'lucide-react';

interface RepositoryUploadProps {
  isOpen: boolean;
  onClose: () => void;
  onUploadSuccess: (repoId: string) => void;
  token: string;
}

const RepositoryUpload: React.FC<RepositoryUploadProps> = ({ 
  isOpen, 
  onClose, 
  onUploadSuccess,
  token 
}) => {
  const [file, setFile] = useState<File | null>(null);
  const [repoName, setRepoName] = useState('');
  const [description, setDescription] = useState('');
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      // Check file type
      const validTypes = ['.zip', '.tar.gz', '.tgz'];
      const isValid = validTypes.some(type => selectedFile.name.endsWith(type));
      
      if (!isValid) {
        setError('Please select a .zip, .tar.gz, or .tgz file');
        return;
      }

      // Check file size (50MB limit)
      if (selectedFile.size > 50 * 1024 * 1024) {
        setError('File size must be less than 50MB');
        return;
      }

      setFile(selectedFile);
      setError('');
      
      // Auto-fill repo name from filename
      if (!repoName) {
        const name = selectedFile.name.replace(/\.(zip|tar\.gz|tgz)$/, '');
        setRepoName(name);
      }
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      const event = {
        target: { files: [droppedFile] }
      } as any;
      handleFileSelect(event);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleUpload = async () => {
    if (!file || !repoName) {
      setError('Please select a file and enter a repository name');
      return;
    }

    setUploading(true);
    setProgress(0);
    setError('');

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('name', repoName);
      if (description) {
        formData.append('description', description);
      }

      const xhr = new XMLHttpRequest();

      // Track upload progress
      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
          const percentComplete = (e.loaded / e.total) * 100;
          setProgress(percentComplete);
        }
      });

      // Handle completion
      xhr.addEventListener('load', () => {
        if (xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          setSuccess(true);
          setTimeout(() => {
            onUploadSuccess(response.id);
            onClose();
            resetForm();
          }, 1500);
        } else {
          const error = JSON.parse(xhr.responseText);
          setError(error.detail || 'Upload failed');
          setUploading(false);
        }
      });

      // Handle errors
      xhr.addEventListener('error', () => {
        setError('Network error occurred');
        setUploading(false);
      });

      xhr.open('POST', 'http://localhost:8000/api/repository/upload');
      xhr.setRequestHeader('Authorization', `Bearer ${token}`);
      xhr.send(formData);

    } catch (err: any) {
      setError(err.message || 'Upload failed');
      setUploading(false);
    }
  };

  const resetForm = () => {
    setFile(null);
    setRepoName('');
    setDescription('');
    setProgress(0);
    setError('');
    setSuccess(false);
    setUploading(false);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="relative w-full max-w-2xl">
              {/* Glassmorphism container */}
              <div className="relative bg-black/40 backdrop-blur-xl border-4 border-white/20 rounded-3xl p-8 shadow-2xl">
                {/* Close button */}
                <button
                  onClick={onClose}
                  className="absolute top-4 right-4 p-2 rounded-xl bg-white/10 hover:bg-white/20 transition-all duration-300 border-2 border-white/20"
                >
                  <X className="w-5 h-5 text-white" />
                </button>

                {/* Title */}
                <motion.div
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                  className="mb-8"
                >
                  <h2 className="text-3xl font-black text-white mb-2">
                    Upload Repository
                  </h2>
                  <p className="text-white/60">
                    Upload a .zip, .tar.gz, or .tgz file of your code repository
                  </p>
                </motion.div>

                {/* Error message */}
                <AnimatePresence>
                  {error && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mb-4 p-4 bg-red-500/20 border-2 border-red-500 rounded-xl flex items-center gap-2"
                    >
                      <AlertCircle className="w-5 h-5 text-red-500" />
                      <p className="text-red-500 text-sm font-semibold">{error}</p>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Success message */}
                <AnimatePresence>
                  {success && (
                    <motion.div
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.9 }}
                      className="mb-4 p-4 bg-green-500/20 border-2 border-green-500 rounded-xl flex items-center gap-2"
                    >
                      <CheckCircle className="w-5 h-5 text-green-500" />
                      <p className="text-green-500 text-sm font-semibold">
                        Repository uploaded successfully!
                      </p>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* File upload area */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="mb-6"
                >
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".zip,.tar.gz,.tgz"
                    onChange={handleFileSelect}
                    className="hidden"
                  />
                  
                  <div
                    onClick={() => fileInputRef.current?.click()}
                    onDrop={handleDrop}
                    onDragOver={handleDragOver}
                    className="relative border-4 border-dashed border-white/20 rounded-2xl p-8 text-center cursor-pointer hover:border-cyan-400 hover:bg-white/5 transition-all duration-300"
                  >
                    {file ? (
                      <div className="flex items-center justify-center gap-4">
                        <File className="w-12 h-12 text-cyan-400" />
                        <div className="text-left">
                          <p className="text-white font-bold">{file.name}</p>
                          <p className="text-white/60 text-sm">
                            {(file.size / 1024 / 1024).toFixed(2)} MB
                          </p>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setFile(null);
                          }}
                          className="p-2 rounded-lg bg-red-500/20 hover:bg-red-500/30 border-2 border-red-500"
                        >
                          <X className="w-4 h-4 text-red-500" />
                        </button>
                      </div>
                    ) : (
                      <>
                        <Upload className="w-16 h-16 text-white/40 mx-auto mb-4" />
                        <p className="text-white font-bold mb-2">
                          Click to upload or drag and drop
                        </p>
                        <p className="text-white/60 text-sm">
                          .zip, .tar.gz, or .tgz files (max 50MB)
                        </p>
                      </>
                    )}
                  </div>
                </motion.div>

                {/* Repository name */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                  className="mb-4"
                >
                  <label className="block text-white font-bold mb-2">
                    Repository Name *
                  </label>
                  <input
                    type="text"
                    value={repoName}
                    onChange={(e) => setRepoName(e.target.value)}
                    placeholder="my-awesome-project"
                    className="w-full px-4 py-3 bg-white/10 border-2 border-white/20 rounded-xl text-white placeholder-white/40 focus:border-cyan-400 focus:outline-none transition-all duration-300"
                  />
                </motion.div>

                {/* Description */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                  className="mb-6"
                >
                  <label className="block text-white font-bold mb-2">
                    Description (optional)
                  </label>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="Brief description of your repository..."
                    rows={3}
                    className="w-full px-4 py-3 bg-white/10 border-2 border-white/20 rounded-xl text-white placeholder-white/40 focus:border-cyan-400 focus:outline-none transition-all duration-300 resize-none"
                  />
                </motion.div>

                {/* Progress bar */}
                <AnimatePresence>
                  {uploading && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mb-6"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-white font-bold">Uploading...</span>
                        <span className="text-cyan-400 font-bold">{Math.round(progress)}%</span>
                      </div>
                      <div className="h-3 bg-white/10 rounded-full overflow-hidden border-2 border-white/20">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${progress}%` }}
                          className="h-full bg-gradient-to-r from-cyan-500 to-blue-500"
                        />
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Upload button */}
                <motion.button
                  onClick={handleUpload}
                  disabled={!file || !repoName || uploading || success}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full py-4 bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-black text-lg rounded-xl border-4 border-white/20 shadow-lg hover:shadow-cyan-500/50 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {uploading ? (
                    <>
                      <Loader className="w-5 h-5 animate-spin" />
                      Uploading...
                    </>
                  ) : success ? (
                    <>
                      <CheckCircle className="w-5 h-5" />
                      Success!
                    </>
                  ) : (
                    <>
                      <Upload className="w-5 h-5" />
                      Upload Repository
                    </>
                  )}
                </motion.button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default RepositoryUpload;

// Made with Bob
