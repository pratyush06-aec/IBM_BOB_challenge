'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

interface NodeDetailsProps {
  node: any
  onClose: () => void
}

export default function NodeDetails({ node, onClose }: NodeDetailsProps) {
  const [aiExplanation, setAiExplanation] = useState<string>('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (node) {
      fetchAIExplanation()
    }
  }, [node?.id])

  const fetchAIExplanation = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/ai/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ node_id: node.id }),
      })
      const data = await response.json()
      setAiExplanation(data.explanation)
    } catch (error) {
      console.error('Error fetching AI explanation:', error)
      setAiExplanation('Unable to load AI explanation')
    } finally {
      setLoading(false)
    }
  }

  if (!node) return null

  const properties = node.properties || {}

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-gray-800">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="inline-block px-3 py-1 bg-blue-600/20 text-blue-400 rounded-full text-xs font-semibold mb-2">
              {node.type}
            </div>
            <h2 className="text-xl font-bold text-white mb-1">{node.label}</h2>
            {properties.description && (
              <p className="text-sm text-gray-400">{properties.description}</p>
            )}
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors ml-4"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* AI Explanation */}
        <div>
          <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">
            🤖 AI Explanation
          </h3>
          <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
            {loading ? (
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                <span className="text-sm text-gray-400">Generating explanation...</span>
              </div>
            ) : (
              <p className="text-sm text-gray-300 leading-relaxed">{aiExplanation}</p>
            )}
          </div>
        </div>

        {/* Properties */}
        <div>
          <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">
            Properties
          </h3>
          <div className="space-y-2">
            {Object.entries(properties).map(([key, value]) => {
              if (key === 'description') return null
              return (
                <div key={key} className="flex justify-between py-2 border-b border-gray-800">
                  <span className="text-sm text-gray-400 capitalize">{key.replace(/_/g, ' ')}</span>
                  <span className="text-sm text-white font-mono">
                    {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                  </span>
                </div>
              )
            })}
          </div>
        </div>

        {/* Quick Actions */}
        <div>
          <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">
            Quick Actions
          </h3>
          <div className="space-y-2">
            <button
              onClick={fetchAIExplanation}
              className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm transition-colors"
            >
              🔄 Regenerate Explanation
            </button>
            <button className="w-full px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg text-sm transition-colors">
              📊 View Connections
            </button>
            <button className="w-full px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg text-sm transition-colors">
              🔍 Find Similar
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

// Made with Bob
