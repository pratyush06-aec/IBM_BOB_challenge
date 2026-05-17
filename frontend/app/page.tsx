'use client'

import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'
import { motion, AnimatePresence } from 'framer-motion'
import { LogIn, Upload, FolderGit2, LogOut, User } from 'lucide-react'

// Dynamically import 3D components (client-side only)
const Graph3D = dynamic(() => import('../components/Graph3D'), { ssr: false })
const NodeDetails = dynamic(() => import('../components/NodeDetails'), { ssr: false })
const AIChat = dynamic(() => import('../components/AIChat'), { ssr: false })
const WorkflowView = dynamic(() => import('../components/WorkflowView'), { ssr: false })
const AnimatedBackground = dynamic(() => import('../components/AnimatedBackground'), { ssr: false })
const FloatingElements = dynamic(() => import('../components/FloatingElements'), { ssr: false })
const AuthModal = dynamic(() => import('../components/AuthModal'), { ssr: false })
const RepositoryUpload = dynamic(() => import('../components/RepositoryUpload'), { ssr: false })
const RepositoryList = dynamic(() => import('../components/RepositoryList'), { ssr: false })

export default function Home() {
  const [selectedNode, setSelectedNode] = useState<any>(null)
  const [showWorkflow, setShowWorkflow] = useState(false)
  const [graphData, setGraphData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  
  // Auth state
  const [isAuthenticated, setIsAuthenticated] = useState(true)
  const [user, setUser] = useState<any>(null)
  const [token, setToken] = useState<string>('')
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [showUploadModal, setShowUploadModal] = useState(false)
  const [showRepositoryList, setShowRepositoryList] = useState(false)
  const [currentRepoId, setCurrentRepoId] = useState<string | null>(null)
  const [refreshRepos, setRefreshRepos] = useState(0)

  // Check for existing auth on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken && storedUser) {
      setToken(storedToken)
      setUser(JSON.parse(storedUser))
      setIsAuthenticated(true)
    }
  }, [])

  // Fetch graph data
  useEffect(() => {
    if (currentRepoId && token) {
      // Fetch specific repository graph
      setLoading(true)
      fetch(`http://localhost:8000/api/repository/${currentRepoId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
        .then(res => {
          if (!res.ok) {
            if (res.status === 401) {
              handleLogout();
            }
            throw new Error(`HTTP error! status: ${res.status}`);
          }
          return res.json();
        })
        .then(data => {
          setGraphData(data)
          setLoading(false)
        })
        .catch(err => {
          console.error('Error loading graph:', err)
          setLoading(false)
        })
    } else {
      // Fetch default sample graph
      fetch('http://localhost:8000/api/graph', {
        headers: {
          'Authorization': `Bearer dummy-token`
        }
      })
        .then(res => {
          if (!res.ok) {
            if (res.status === 401) {
              handleLogout();
            }
            throw new Error(`HTTP error! status: ${res.status}`);
          }
          return res.json();
        })
        .then(data => {
          setGraphData(data)
          setLoading(false)
        })
        .catch(err => {
          console.error('Error loading graph:', err)
          setLoading(false)
        })
    } else {
        setLoading(false)
    }
  }, [currentRepoId, token])

  const handleAuthSuccess = (newToken: string, newUser: any) => {
    setToken(newToken)
    setUser(newUser)
    setIsAuthenticated(true)
    setShowAuthModal(false)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setToken('')
    setUser(null)
    setIsAuthenticated(false)
    setCurrentRepoId(null)
  }

  const handleUploadSuccess = (repoId: string) => {
    setCurrentRepoId(repoId)
    setRefreshRepos(prev => prev + 1)
    setShowUploadModal(false)
    setShowRepositoryList(false)
  }

  const handleSelectRepository = (repoId: string) => {
    setCurrentRepoId(repoId)
    setShowRepositoryList(false)
  }

  return (
    <main className="min-h-screen relative overflow-hidden">
      {/* 3D Animated Background */}
      <AnimatedBackground />
      
      {/* Floating Elements with Parallax */}
      <FloatingElements />
      
      {/* Glassmorphism overlay */}
      <div className="fixed inset-0 bg-gradient-to-br from-blue-500/5 via-purple-500/5 to-pink-500/5 pointer-events-none" />
      
      {/* Header with glassmorphism */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-black/30 backdrop-blur-xl border-b border-white/10 shadow-lg shadow-blue-500/10">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{
                duration: 0.8,
                ease: [0.6, 0.05, 0.01, 0.9],
                delay: 0.1
              }}
              className="flex items-center space-x-3"
            >
              <motion.div
                className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center"
                whileHover={{
                  scale: 1.1,
                  rotate: 5,
                  boxShadow: "0 0 25px rgba(59, 130, 246, 0.6)"
                }}
                transition={{ type: "spring", stiffness: 400, damping: 10 }}
              >
                <motion.span
                  className="text-white font-bold text-xl"
                  animate={{
                    scale: [1, 1.1, 1],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeInOut"
                  }}
                >
                  G
                </motion.span>
              </motion.div>
              <div>
                <motion.h1
                  className="text-2xl font-bold text-white"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3, duration: 0.6 }}
                >
                  GraphMind AI
                </motion.h1>
                <motion.p
                  className="text-xs text-gray-400"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.5, duration: 0.6 }}
                >
                  Engineering Cognition Platform
                </motion.p>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{
                duration: 0.8,
                ease: [0.6, 0.05, 0.01, 0.9],
                delay: 0.2
              }}
              className="flex items-center space-x-4"
            >
              {isAuthenticated ? (
                <>
                  {/* Repository List Button */}
                  <motion.button
                    onClick={() => setShowRepositoryList(!showRepositoryList)}
                    className="px-4 py-2.5 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-xl font-semibold shadow-lg shadow-purple-500/30 flex items-center gap-2"
                    whileHover={{
                      scale: 1.05,
                      boxShadow: "0 20px 40px rgba(168, 85, 247, 0.4)"
                    }}
                    whileTap={{ scale: 0.95 }}
                    transition={{ type: "spring", stiffness: 400, damping: 17 }}
                  >
                    <FolderGit2 className="w-4 h-4" />
                    Repositories
                  </motion.button>

                  {/* Upload Button */}
                  <motion.button
                    onClick={() => setShowUploadModal(true)}
                    className="px-4 py-2.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-700 hover:to-blue-700 text-white rounded-xl font-semibold shadow-lg shadow-cyan-500/30 flex items-center gap-2"
                    whileHover={{
                      scale: 1.05,
                      boxShadow: "0 20px 40px rgba(6, 182, 212, 0.4)"
                    }}
                    whileTap={{ scale: 0.95 }}
                    transition={{ type: "spring", stiffness: 400, damping: 17 }}
                  >
                    <Upload className="w-4 h-4" />
                    Upload
                  </motion.button>

                  {/* Workflow Toggle */}
                  <motion.button
                    onClick={() => setShowWorkflow(!showWorkflow)}
                    className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-xl font-semibold shadow-lg shadow-blue-500/30"
                    whileHover={{
                      scale: 1.05,
                      boxShadow: "0 20px 40px rgba(59, 130, 246, 0.4)"
                    }}
                    whileTap={{ scale: 0.95 }}
                    transition={{ type: "spring", stiffness: 400, damping: 17 }}
                  >
                    <motion.span
                      animate={{ opacity: [1, 0.7, 1] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    >
                      {showWorkflow ? '✨ Show Graph' : '🔮 Show Workflows'}
                    </motion.span>
                  </motion.button>

                  {/* User Menu */}
                  <div className="flex items-center gap-3 px-4 py-2 bg-white/10 rounded-xl border border-white/20">
                    <User className="w-4 h-4 text-white" />
                    <span className="text-white font-semibold">{user?.username}</span>
                    <motion.button
                      onClick={handleLogout}
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      className="p-1.5 rounded-lg bg-red-500/20 hover:bg-red-500/30 border border-red-500"
                    >
                      <LogOut className="w-4 h-4 text-red-400" />
                    </motion.button>
                  </div>
                </>
              ) : (
                <motion.button
                  onClick={() => setShowAuthModal(true)}
                  className="px-6 py-2.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-700 hover:to-blue-700 text-white rounded-xl font-semibold shadow-lg shadow-cyan-500/30 flex items-center gap-2"
                  whileHover={{
                    scale: 1.05,
                    boxShadow: "0 20px 40px rgba(6, 182, 212, 0.4)"
                  }}
                  whileTap={{ scale: 0.95 }}
                  transition={{ type: "spring", stiffness: 400, damping: 17 }}
                >
                  <LogIn className="w-4 h-4" />
                  Sign In
                </motion.button>
              )}
            </motion.div>
          </div>
        </div>
      </header>

      {/* Repository List Sidebar */}
      <AnimatePresence>
        {showRepositoryList && isAuthenticated && (
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: "spring", damping: 25, stiffness: 200 }}
            className="fixed top-20 right-0 bottom-0 w-96 bg-black/40 backdrop-blur-xl border-l border-white/10 shadow-2xl z-40 overflow-y-auto"
          >
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-black text-white">Your Repositories</h2>
                <motion.button
                  onClick={() => setShowRepositoryList(false)}
                  whileHover={{ scale: 1.1, rotate: 90 }}
                  whileTap={{ scale: 0.9 }}
                  className="p-2 rounded-xl bg-white/10 hover:bg-white/20 border-2 border-white/20"
                >
                  <span className="text-white text-xl">×</span>
                </motion.button>
              </div>
              <RepositoryList
                token={token}
                onSelectRepository={handleSelectRepository}
                refreshTrigger={refreshRepos}
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <div className="pt-20 h-screen flex">
        {/* Left Sidebar - Node Details */}
        {selectedNode && (
          <motion.div
            initial={{ x: -300, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -300, opacity: 0 }}
            className="w-96 bg-black/40 backdrop-blur-2xl border-r border-white/10 overflow-y-auto shadow-2xl shadow-blue-500/20"
            style={{
              background: 'linear-gradient(135deg, rgba(0,0,0,0.4) 0%, rgba(30,27,75,0.4) 100%)',
            }}
          >
            <NodeDetails
              node={selectedNode}
              onClose={() => setSelectedNode(null)}
            />
          </motion.div>
        )}

        {/* Center - 3D Graph or Workflow View */}
        <div className="flex-1 relative">
          {loading ? (
            <motion.div
              className="flex items-center justify-center h-full"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              <div className="text-center">
                <motion.div
                  className="relative w-24 h-24 mx-auto mb-6"
                  animate={{
                    rotate: 360,
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: "linear"
                  }}
                >
                  <motion.div
                    className="absolute inset-0 border-4 border-blue-500/30 rounded-full"
                    animate={{
                      scale: [1, 1.2, 1],
                      opacity: [0.3, 0.6, 0.3],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      ease: "easeInOut"
                    }}
                  />
                  <motion.div
                    className="absolute inset-0 border-4 border-t-blue-500 border-r-purple-500 border-b-transparent border-l-transparent rounded-full"
                    animate={{
                      rotate: 360,
                    }}
                    transition={{
                      duration: 1.5,
                      repeat: Infinity,
                      ease: "linear"
                    }}
                  />
                </motion.div>
                <motion.p
                  className="text-gray-300 text-lg font-semibold"
                  animate={{
                    opacity: [0.5, 1, 0.5],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeInOut"
                  }}
                >
                  Loading graph data...
                </motion.p>
                <motion.div
                  className="flex justify-center gap-2 mt-4"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.5 }}
                >
                  {[0, 1, 2].map((i) => (
                    <motion.div
                      key={i}
                      className="w-2 h-2 bg-blue-500 rounded-full"
                      animate={{
                        y: [0, -10, 0],
                        opacity: [0.3, 1, 0.3],
                      }}
                      transition={{
                        duration: 1,
                        repeat: Infinity,
                        delay: i * 0.2,
                        ease: "easeInOut"
                      }}
                    />
                  ))}
                </motion.div>
              </div>
            </motion.div>
          ) : showWorkflow ? (
            <WorkflowView token={token} />
          ) : (
            <Graph3D
              data={graphData}
              onNodeClick={setSelectedNode}
              selectedNode={selectedNode}
            />
          )}


          {/* Stats Overlay */}
          {!loading && graphData && !showWorkflow && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="absolute top-6 left-6 bg-black/40 backdrop-blur-xl rounded-2xl p-6 border-2 border-white/20 shadow-2xl shadow-purple-500/20"
              style={{
                background: 'linear-gradient(135deg, rgba(0,0,0,0.5) 0%, rgba(59,130,246,0.2) 100%)',
              }}
            >
              <h3 className="text-white font-bold text-lg mb-3 drop-shadow-lg">
                {currentRepoId ? 'Repository Graph' : 'E-Commerce System'}
              </h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="bg-white/10 rounded-lg p-3 border border-white/20">
                  <p className="text-blue-300 font-semibold">Nodes</p>
                  <p className="text-white font-bold text-2xl">{graphData.nodes?.length || 0}</p>
                </div>
                <div className="bg-white/10 rounded-lg p-3 border border-white/20">
                  <p className="text-purple-300 font-semibold">Edges</p>
                  <p className="text-white font-bold text-2xl">{graphData.edges?.length || 0}</p>
                </div>
              </div>
            </motion.div>
          )}
        </div>

        {/* Right Sidebar - AI Chat with glassmorphism */}
        <motion.div
          initial={{ x: 400, opacity: 0, scale: 0.9 }}
          animate={{
            x: 0,
            opacity: 1,
            scale: 1,
          }}
          transition={{
            duration: 0.6,
            ease: [0.16, 1, 0.3, 1],
            delay: 0.1,
            opacity: { duration: 0.4 }
          }}
          className="w-96 bg-black/40 backdrop-blur-2xl border-l border-white/10 shadow-2xl shadow-purple-500/20"
          style={{
            background: 'linear-gradient(135deg, rgba(0,0,0,0.4) 0%, rgba(88,28,135,0.3) 100%)',
          }}
          whileHover={{
            boxShadow: "0 25px 50px -12px rgba(168, 85, 247, 0.3)"
          }}
        >
          <AIChat selectedNode={selectedNode} />
        </motion.div>
      </div>

      {/* Modals */}
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onAuthSuccess={handleAuthSuccess}
      />

      <RepositoryUpload
        isOpen={showUploadModal}
        onClose={() => setShowUploadModal(false)}
        onUploadSuccess={handleUploadSuccess}
        token={token}
      />
    </main>
  )
}

// Made with Bob
