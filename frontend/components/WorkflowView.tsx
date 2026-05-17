'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

interface Workflow {
  id: string
  name: string
  description: string
  steps: Array<{
    step: number
    node_id: string
    description: string
    node?: any
  }>
}

interface WorkflowViewProps {
  token: string
}

export default function WorkflowView({ token }: WorkflowViewProps) {
  const [workflows, setWorkflows] = useState<Workflow[]>([])
  const [selectedWorkflow, setSelectedWorkflow] = useState<Workflow | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchWorkflows()
  }, [])

  const fetchWorkflows = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/workflows`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      const data = await response.json()
      setWorkflows(data.workflows || [])
      if (data.workflows && data.workflows.length > 0) {
        fetchWorkflowDetails(data.workflows[0].id)
      }
    } catch (error) {
      console.error('Error fetching workflows:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchWorkflowDetails = async (workflowId: string) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/workflow/${workflowId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      const data = await response.json()
      setSelectedWorkflow(data)
    } catch (error) {
      console.error('Error fetching workflow details:', error)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-400">Loading workflows...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full flex">
      {/* Workflow List */}
      <div className="w-80 bg-gray-900/50 border-r border-gray-800 p-6 overflow-y-auto">
        <h2 className="text-xl font-bold text-white mb-4">Workflows</h2>
        <div className="space-y-3">
          {workflows.map((workflow) => (
            <motion.button
              key={workflow.id}
              onClick={() => fetchWorkflowDetails(workflow.id)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className={`w-full text-left p-4 rounded-lg border transition-all ${
                selectedWorkflow?.id === workflow.id
                  ? 'bg-purple-600/20 border-purple-600'
                  : 'bg-gray-800/50 border-gray-700 hover:border-gray-600'
              }`}
            >
              <h3 className="font-semibold text-white mb-1">{workflow.name}</h3>
              <p className="text-sm text-gray-400">{workflow.description}</p>
              <div className="mt-2 text-xs text-gray-500">
                {workflow.steps?.length || 0} steps
              </div>
            </motion.button>
          ))}
        </div>
      </div>

      {/* Workflow Details */}
      <div className="flex-1 p-8 overflow-y-auto">
        {selectedWorkflow ? (
          <div>
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-white mb-2">{selectedWorkflow.name}</h1>
              <p className="text-gray-400">{selectedWorkflow.description}</p>
            </div>

            {/* Workflow Steps */}
            <div className="relative">
              {/* Vertical Line */}
              <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gradient-to-b from-purple-500 via-blue-500 to-green-500"></div>

              {/* Steps */}
              <div className="space-y-6">
                {selectedWorkflow.steps.map((step, index) => (
                  <motion.div
                    key={step.step}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="relative pl-16"
                  >
                    {/* Step Number */}
                    <div className="absolute left-0 w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-600 rounded-full flex items-center justify-center text-white font-bold shadow-lg">
                      {step.step}
                    </div>

                    {/* Step Content */}
                    <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-6 hover:border-gray-600 transition-colors">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h3 className="text-lg font-semibold text-white mb-1">
                            {step.description}
                          </h3>
                          {step.node && (
                            <div className="flex items-center space-x-2 mt-2">
                              <span className="px-2 py-1 bg-blue-600/20 text-blue-400 rounded text-xs">
                                {step.node.type}
                              </span>
                              <span className="text-sm text-gray-400">
                                {step.node.label}
                              </span>
                            </div>
                          )}
                        </div>
                        <div className="text-2xl">
                          {getStepIcon(index, selectedWorkflow.steps.length)}
                        </div>
                      </div>

                      {step.node?.properties?.description && (
                        <p className="text-sm text-gray-400 mt-2">
                          {step.node.properties.description}
                        </p>
                      )}

                      {/* Step Metadata */}
                      {step.node && (
                        <div className="mt-4 pt-4 border-t border-gray-700 grid grid-cols-2 gap-4 text-xs">
                          {step.node.properties?.file_path && (
                            <div>
                              <span className="text-gray-500">File:</span>
                              <span className="text-gray-300 ml-2 font-mono">
                                {step.node.properties.file_path}
                              </span>
                            </div>
                          )}
                          {step.node.properties?.method && (
                            <div>
                              <span className="text-gray-500">Method:</span>
                              <span className="text-gray-300 ml-2 font-mono">
                                {step.node.properties.method}
                              </span>
                            </div>
                          )}
                        </div>
                      )}
                    </div>

                    {/* Arrow */}
                    {index < selectedWorkflow.steps.length - 1 && (
                      <div className="absolute left-6 -bottom-3 w-0 h-0 border-l-8 border-r-8 border-t-8 border-l-transparent border-r-transparent border-t-purple-500 transform -translate-x-1/2"></div>
                    )}
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Workflow Summary */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="mt-8 p-6 bg-gradient-to-r from-purple-900/20 to-blue-900/20 border border-purple-700/30 rounded-lg"
            >
              <h3 className="text-lg font-semibold text-white mb-2">Workflow Summary</h3>
              <div className="grid grid-cols-3 gap-4 text-sm">
                <div>
                  <p className="text-gray-400">Total Steps</p>
                  <p className="text-2xl font-bold text-white">{selectedWorkflow.steps.length}</p>
                </div>
                <div>
                  <p className="text-gray-400">Services Involved</p>
                  <p className="text-2xl font-bold text-white">
                    {new Set(selectedWorkflow.steps.map(s => s.node?.type).filter(Boolean)).size}
                  </p>
                </div>
                <div>
                  <p className="text-gray-400">Complexity</p>
                  <p className="text-2xl font-bold text-white">
                    {selectedWorkflow.steps.length > 5 ? 'High' : 'Medium'}
                  </p>
                </div>
              </div>
            </motion.div>
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-400">Select a workflow to view details</p>
          </div>
        )}
      </div>
    </div>
  )
}

function getStepIcon(index: number, total: number): string {
  const icons = ['🚀', '⚙️', '🔍', '💳', '📦', '✅', '📧']
  return icons[index % icons.length]
}

// Made with Bob
