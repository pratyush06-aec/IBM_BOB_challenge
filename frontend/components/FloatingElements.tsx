'use client'

import { motion } from 'framer-motion'

export default function FloatingElements() {
  const elements = [
    { size: 60, color: 'from-blue-500/20 to-cyan-500/20', delay: 0, duration: 20, x: '10%', y: '20%' },
    { size: 80, color: 'from-purple-500/20 to-pink-500/20', delay: 2, duration: 25, x: '80%', y: '15%' },
    { size: 50, color: 'from-green-500/20 to-emerald-500/20', delay: 4, duration: 22, x: '15%', y: '70%' },
    { size: 70, color: 'from-orange-500/20 to-yellow-500/20', delay: 1, duration: 23, x: '85%', y: '75%' },
    { size: 40, color: 'from-pink-500/20 to-rose-500/20', delay: 3, duration: 21, x: '50%', y: '40%' },
    { size: 55, color: 'from-indigo-500/20 to-blue-500/20', delay: 5, duration: 24, x: '30%', y: '85%' },
  ]

  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden -z-5">
      {elements.map((el, index) => (
        <motion.div
          key={index}
          className={`absolute rounded-full bg-gradient-to-br ${el.color} blur-3xl`}
          style={{
            width: el.size,
            height: el.size,
            left: el.x,
            top: el.y,
          }}
          animate={{
            y: [0, -30, 0],
            x: [0, 20, 0],
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.6, 0.3],
          }}
          transition={{
            duration: el.duration,
            repeat: Infinity,
            delay: el.delay,
            ease: "easeInOut",
          }}
        />
      ))}
      
      {/* Animated gradient orbs */}
      <motion.div
        className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-full blur-3xl"
        animate={{
          scale: [1, 1.3, 1],
          opacity: [0.2, 0.4, 0.2],
          rotate: [0, 180, 360],
        }}
        transition={{
          duration: 30,
          repeat: Infinity,
          ease: "linear",
        }}
      />
      
      <motion.div
        className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-gradient-to-r from-purple-500/10 to-pink-500/10 rounded-full blur-3xl"
        animate={{
          scale: [1, 1.4, 1],
          opacity: [0.2, 0.5, 0.2],
          rotate: [360, 180, 0],
        }}
        transition={{
          duration: 35,
          repeat: Infinity,
          ease: "linear",
        }}
      />

      {/* Floating particles */}
      {Array.from({ length: 20 }).map((_, i) => (
        <motion.div
          key={`particle-${i}`}
          className="absolute w-1 h-1 bg-white/40 rounded-full"
          style={{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
          }}
          animate={{
            y: [0, -100, 0],
            opacity: [0, 1, 0],
          }}
          transition={{
            duration: 5 + Math.random() * 5,
            repeat: Infinity,
            delay: Math.random() * 5,
            ease: "easeInOut",
          }}
        />
      ))}
    </div>
  )
}

// Made with Bob