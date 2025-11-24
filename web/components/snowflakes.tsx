'use client'

import { useEffect, useState } from 'react'

interface Snowflake {
  id: number
  left: number
  animationDuration: number
  animationDelay: number
  size: number
  opacity: number
}

export function Snowflakes() {
  const [snowflakes, setSnowflakes] = useState<Snowflake[]>([])

  useEffect(() => {
    const flakes: Snowflake[] = Array.from({ length: 50 }, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      animationDuration: 10 + Math.random() * 20,
      animationDelay: Math.random() * 10,
      size: 2 + Math.random() * 4,
      opacity: 0.3 + Math.random() * 0.7,
    }))
    setSnowflakes(flakes)
  }, [])

  return (
    <div className="pointer-events-none fixed inset-0 z-50">
      {snowflakes.map((flake) => (
        <div
          key={flake.id}
          className="absolute animate-fall"
          style={{
            left: `${flake.left}%`,
            animationDuration: `${flake.animationDuration}s`,
            animationDelay: `${flake.animationDelay}s`,
            opacity: flake.opacity,
          }}
        >
          <div
            className="bg-white"
            style={{
              width: `${flake.size}px`,
              height: `${flake.size}px`,
              borderRadius: '50%',
              boxShadow: '0 0 4px rgba(255, 255, 255, 0.8)',
            }}
          />
        </div>
      ))}
    </div>
  )
}
