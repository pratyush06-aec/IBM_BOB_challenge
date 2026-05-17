'use client'

import { useEffect, useRef } from 'react'
import * as THREE from 'three'

export default function AnimatedBackground() {
  const containerRef = useRef<HTMLDivElement>(null)
  const sceneRef = useRef<THREE.Scene | null>(null)
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null)
  const animationIdRef = useRef<number | null>(null)

  useEffect(() => {
    if (!containerRef.current) return

    // Scene setup
    const scene = new THREE.Scene()
    sceneRef.current = scene
    
    const camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    )
    camera.position.z = 30

    // Renderer setup
    const renderer = new THREE.WebGLRenderer({ 
      alpha: true, 
      antialias: true 
    })
    renderer.setSize(window.innerWidth, window.innerHeight)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    containerRef.current.appendChild(renderer.domElement)
    rendererRef.current = renderer

    // Create animated geometric shapes
    const geometries = [
      new THREE.IcosahedronGeometry(1, 0),
      new THREE.OctahedronGeometry(1, 0),
      new THREE.TetrahedronGeometry(1, 0),
      new THREE.TorusGeometry(0.8, 0.3, 16, 100),
    ]

    const materials = [
      new THREE.MeshPhongMaterial({ 
        color: 0x0EA5E9, 
        wireframe: true, 
        transparent: true, 
        opacity: 0.15 
      }),
      new THREE.MeshPhongMaterial({ 
        color: 0x10B981, 
        wireframe: true, 
        transparent: true, 
        opacity: 0.15 
      }),
      new THREE.MeshPhongMaterial({ 
        color: 0xA855F7, 
        wireframe: true, 
        transparent: true, 
        opacity: 0.15 
      }),
      new THREE.MeshPhongMaterial({ 
        color: 0xF59E0B, 
        wireframe: true, 
        transparent: true, 
        opacity: 0.15 
      }),
    ]

    const meshes: THREE.Mesh[] = []
    
    // Create multiple floating shapes
    for (let i = 0; i < 15; i++) {
      const geometry = geometries[Math.floor(Math.random() * geometries.length)]
      const material = materials[Math.floor(Math.random() * materials.length)]
      const mesh = new THREE.Mesh(geometry, material)
      
      // Random position
      mesh.position.x = (Math.random() - 0.5) * 50
      mesh.position.y = (Math.random() - 0.5) * 50
      mesh.position.z = (Math.random() - 0.5) * 30
      
      // Random scale
      const scale = Math.random() * 2 + 1
      mesh.scale.set(scale, scale, scale)
      
      // Store rotation speed
      mesh.userData.rotationSpeed = {
        x: (Math.random() - 0.5) * 0.02,
        y: (Math.random() - 0.5) * 0.02,
        z: (Math.random() - 0.5) * 0.02,
      }
      
      scene.add(mesh)
      meshes.push(mesh)
    }

    // Add ambient light
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
    scene.add(ambientLight)

    // Add directional lights for depth
    const light1 = new THREE.DirectionalLight(0x0EA5E9, 0.8)
    light1.position.set(5, 5, 5)
    scene.add(light1)

    const light2 = new THREE.DirectionalLight(0xA855F7, 0.6)
    light2.position.set(-5, -5, -5)
    scene.add(light2)

    // Add particles for extra effect
    const particlesGeometry = new THREE.BufferGeometry()
    const particlesCount = 1000
    const positions = new Float32Array(particlesCount * 3)

    for (let i = 0; i < particlesCount * 3; i++) {
      positions[i] = (Math.random() - 0.5) * 100
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    
    const particlesMaterial = new THREE.PointsMaterial({
      color: 0x60A5FA,
      size: 0.1,
      transparent: true,
      opacity: 0.6,
      blending: THREE.AdditiveBlending,
    })

    const particles = new THREE.Points(particlesGeometry, particlesMaterial)
    scene.add(particles)

    // Animation loop
    let time = 0
    const animate = () => {
      animationIdRef.current = requestAnimationFrame(animate)
      time += 0.001

      // Rotate meshes
      meshes.forEach((mesh) => {
        mesh.rotation.x += mesh.userData.rotationSpeed.x
        mesh.rotation.y += mesh.userData.rotationSpeed.y
        mesh.rotation.z += mesh.userData.rotationSpeed.z
        
        // Floating animation
        mesh.position.y += Math.sin(time * 2 + mesh.position.x) * 0.01
      })

      // Rotate particles
      particles.rotation.y += 0.0005
      particles.rotation.x += 0.0003

      // Gentle camera movement
      camera.position.x = Math.sin(time * 0.5) * 2
      camera.position.y = Math.cos(time * 0.3) * 2
      camera.lookAt(0, 0, 0)

      renderer.render(scene, camera)
    }

    animate()

    // Handle resize
    const handleResize = () => {
      if (!containerRef.current || !rendererRef.current) return
      
      camera.aspect = window.innerWidth / window.innerHeight
      camera.updateProjectionMatrix()
      rendererRef.current.setSize(window.innerWidth, window.innerHeight)
    }

    window.addEventListener('resize', handleResize)

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize)
      
      if (animationIdRef.current) {
        cancelAnimationFrame(animationIdRef.current)
      }
      
      if (rendererRef.current && containerRef.current) {
        containerRef.current.removeChild(rendererRef.current.domElement)
        rendererRef.current.dispose()
      }
      
      meshes.forEach(mesh => {
        mesh.geometry.dispose()
        if (Array.isArray(mesh.material)) {
          mesh.material.forEach(mat => mat.dispose())
        } else {
          mesh.material.dispose()
        }
      })
      
      particlesGeometry.dispose()
      particlesMaterial.dispose()
    }
  }, [])

  return (
    <div 
      ref={containerRef} 
      className="fixed inset-0 -z-10"
      style={{
        background: 'radial-gradient(ellipse at top, #1e1b4b 0%, #000000 50%, #0f172a 100%)',
      }}
    />
  )
}

// Made with Bob