'use client'

import { useRef, useEffect, useState, useCallback } from 'react'
import ForceGraph3D from 'react-force-graph-3d'
import * as THREE from 'three'

interface Node {
  id: string
  type: string
  label: string
  properties: any
  position?: { x: number; y: number; z: number }
}

interface Edge {
  id: string
  source: string
  target: string
  type: string
  label: string
  properties: any
}

interface GraphData {
  nodes: Node[]
  edges: Edge[]
}

interface Graph3DProps {
  data: GraphData | null
  onNodeClick: (node: Node | null) => void
  selectedNode: Node | null
}

// Bold, high-contrast color mapping for node types with neo-brutalism style
const NODE_COLORS: Record<string, string> = {
  Service: '#0EA5E9',    // Bright Cyan
  API: '#10B981',        // Bright Green
  Function: '#A855F7',   // Bright Purple
  Database: '#F59E0B',   // Bright Orange
  Cache: '#EF4444',      // Bright Red
  Queue: '#EC4899',      // Bright Pink
}

// Bold border colors for high contrast
const NODE_BORDER_COLORS: Record<string, string> = {
  Service: '#06B6D4',
  API: '#059669',
  Function: '#9333EA',
  Database: '#D97706',
  Cache: '#DC2626',
  Queue: '#DB2777',
}

export default function Graph3D({ data, onNodeClick, selectedNode }: Graph3DProps) {
  const fgRef = useRef<any>()
  const [graphData, setGraphData] = useState<any>(null)
  const draggedNodeRef = useRef<any>(null)
  const controlsPatchedRef = useRef(false)

  // Patch OrbitControls immediately when graph is ready
  useEffect(() => {
    if (!fgRef.current || controlsPatchedRef.current) return

    const patchControls = () => {
      try {
        const controls = fgRef.current?.controls()
        if (controls && controls.constructor.name === 'OrbitControls' && !controlsPatchedRef.current) {
          // Check if onPointerUp exists before patching
          if (typeof controls.onPointerUp !== 'function') {
            return
          }
          
          const originalOnPointerUp = controls.onPointerUp.bind(controls)
          
          controls.onPointerUp = function(event: any) {
            try {
              // Check if pointer state exists and is valid
              if (this.pointers && this.pointers.length > 0 && this.pointers[0]) {
                originalOnPointerUp(event)
              }
            } catch (error) {
              // Silently handle the error - prevents crash from DragControls conflict
            }
          }
          
          controlsPatchedRef.current = true
        }
      } catch (error) {
        // Silently wait for controls to initialize
      }
    }

    // Try patching immediately and with retries
    patchControls()
    const timer1 = setTimeout(patchControls, 100)
    const timer2 = setTimeout(patchControls, 300)
    const timer3 = setTimeout(patchControls, 500)

    return () => {
      clearTimeout(timer1)
      clearTimeout(timer2)
      clearTimeout(timer3)
    }
  }, [graphData])

  useEffect(() => {
    if (!data) return

    // Transform data for ForceGraph3D with bold styling
    const transformedData = {
      nodes: data.nodes.map(node => ({
        ...node,
        color: NODE_COLORS[node.type] || '#6b7280',
        borderColor: NODE_BORDER_COLORS[node.type] || '#374151',
        val: node.type === 'Service' ? 25 : node.type === 'API' ? 20 : 15,
      })),
      links: data.edges.map(edge => ({
        ...edge,
        source: edge.source,
        target: edge.target,
        color: '#60A5FA', // Bright blue for visibility
        width: 2,
      })),
    }

    setGraphData(transformedData)

    // Center camera after a short delay
    setTimeout(() => {
      if (fgRef.current) {
        fgRef.current.zoomToFit(400)
      }
    }, 500)
  }, [data])

  // Handle node drag - this prevents the click event from firing
  const handleNodeDrag = useCallback((node: any) => {
    draggedNodeRef.current = node
  }, [])

  const handleNodeClick = useCallback((node: any) => {
    // If we just dragged this node, don't trigger click
    if (draggedNodeRef.current === node) {
      draggedNodeRef.current = null
      return
    }

    onNodeClick(node)
    
    // Focus camera on node with safety checks
    if (fgRef.current && node.x !== undefined && node.y !== undefined && node.z !== undefined) {
      const distance = 200
      const distRatio = 1 + distance / Math.hypot(node.x, node.y, node.z)
      
      fgRef.current.cameraPosition(
        { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio },
        node,
        1000
      )
    }
  }, [onNodeClick])

  const handleBackgroundClick = useCallback(() => {
    onNodeClick(null)
  }, [onNodeClick])

  if (!graphData) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-gray-400">Loading graph...</p>
      </div>
    )
  }

  return (
    <div className="w-full h-full">
      <ForceGraph3D
        ref={fgRef}
        graphData={graphData}
        nodeLabel={(node: any) => `
          <div style="
            background: rgba(0, 0, 0, 0.9);
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #374151;
            color: white;
            font-family: Arial, sans-serif;
            max-width: 250px;
          ">
            <div style="font-weight: bold; font-size: 14px; margin-bottom: 4px;">
              ${node.label}
            </div>
            <div style="font-size: 11px; color: #9ca3af; margin-bottom: 8px;">
              ${node.type}
            </div>
            <div style="font-size: 11px; color: #d1d5db;">
              ${node.properties?.description || 'No description'}
            </div>
          </div>
        `}
        nodeColor={(node: any) =>
          selectedNode?.id === node.id ? '#fbbf24' : node.color
        }
        nodeVal={(node: any) =>
          selectedNode?.id === node.id ? node.val * 1.5 : node.val
        }
        nodeThreeObject={(node: any) => {
          const isSelected = selectedNode?.id === node.id
          const sprite = new THREE.Sprite(
            new THREE.SpriteMaterial({
              map: new THREE.CanvasTexture(generateNodeTexture(node, isSelected)),
              transparent: true,
            })
          )
          sprite.scale.set(isSelected ? 20 : 12, isSelected ? 20 : 12, 1)
          return sprite
        }}
        linkLabel={(link: any) => `
          <div style="
            background: rgba(0, 0, 0, 0.9);
            padding: 8px;
            border-radius: 6px;
            border: 1px solid #374151;
            color: white;
            font-family: Arial, sans-serif;
            font-size: 11px;
          ">
            ${link.type}
          </div>
        `}
        linkColor={(link: any) => link.color}
        linkWidth={3}
        linkOpacity={0.8}
        linkDirectionalArrowLength={6}
        linkDirectionalArrowRelPos={1}
        linkDirectionalParticles={4}
        linkDirectionalParticleWidth={3}
        linkDirectionalParticleSpeed={0.006}
        onNodeClick={handleNodeClick}
        onNodeDrag={handleNodeDrag}
        onBackgroundClick={handleBackgroundClick}
        backgroundColor="rgba(0, 0, 0, 0)"
        showNavInfo={false}
        enableNodeDrag={true}
        enableNavigationControls={true}
        controlType="orbit"
        d3AlphaDecay={0.02}
        d3VelocityDecay={0.3}
        warmupTicks={100}
        cooldownTicks={0}
      />
    </div>
  )
}

// Generate bold, high-contrast node texture with neo-brutalism style
function generateNodeTexture(node: any, isSelected: boolean): HTMLCanvasElement {
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')!
  const size = 256
  canvas.width = size
  canvas.height = size

  const centerX = size / 2
  const centerY = size / 2
  const radius = size / 2 - 15

  // Add glow effect for selected nodes
  if (isSelected) {
    const gradient = ctx.createRadialGradient(centerX, centerY, radius * 0.5, centerX, centerY, radius * 1.3)
    gradient.addColorStop(0, 'rgba(251, 191, 36, 0.3)')
    gradient.addColorStop(1, 'rgba(251, 191, 36, 0)')
    ctx.fillStyle = gradient
    ctx.fillRect(0, 0, size, size)
  }

  // Draw main circle with bold color
  ctx.beginPath()
  ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI)
  ctx.fillStyle = isSelected ? '#FCD34D' : (NODE_COLORS[node.type] || '#6b7280')
  ctx.fill()

  // Draw bold border with neo-brutalism style
  ctx.strokeStyle = isSelected ? '#000000' : (NODE_BORDER_COLORS[node.type] || '#374151')
  ctx.lineWidth = isSelected ? 12 : 8
  ctx.stroke()

  // Add inner shadow for depth
  ctx.beginPath()
  ctx.arc(centerX, centerY, radius - 6, 0, 2 * Math.PI)
  ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)'
  ctx.lineWidth = 3
  ctx.stroke()

  // Draw icon/text with bold styling
  ctx.fillStyle = isSelected ? '#000000' : '#FFFFFF'
  ctx.font = 'bold 90px Arial'
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'
  ctx.shadowColor = 'rgba(0, 0, 0, 0.5)'
  ctx.shadowBlur = 4
  ctx.shadowOffsetX = 2
  ctx.shadowOffsetY = 2
  
  const icon = getNodeIcon(node.type)
  ctx.fillText(icon, centerX, centerY)

  return canvas
}

// Get icon for node type
function getNodeIcon(type: string): string {
  const icons: Record<string, string> = {
    Service: '⚙️',
    API: '🌐',
    Function: '⚡',
    Database: '💾',
    Cache: '⚡',
    Queue: '📬',
  }
  return icons[type] || '●'
}

// Made with Bob
