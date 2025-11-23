'use client'

import { useState } from 'react'
import { AnimationList } from '@/components/animation-list'
import { TreeVisualizer } from '@/components/tree-visualizer'
import { Sparkles } from '@/components/sparkles'
import { Snowflakes } from '@/components/snowflakes'

import animations from "../../data/animations.json"

export type Animation = {
  name: string
  full_name: string
  speed: number
}


export default function Home() {
  const [selectedAnimation, setSelectedAnimation] = useState<Animation>(animations[0])

  return (
    <div className="min-h-screen bg-background">
      <Sparkles />
      <Snowflakes />
      <header className="bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-8 lg:py-12">
          <div className="space-y-2">
            <h1 className="font-bold text-4xl text-balance text-foreground lg:text-5xl">
              3D eglītes lampiņas
            </h1>
            <p className="text-lg text-muted-foreground lg:text-xl">
              No saraksta izvēlies animāciju, kas tiks atskaņota uz eglītes lampiņām.
              <br />
              Katrai lampiņai ir zināmas 3D koordinātas un animācijas uz eglītes atskaņojās kā uz telpisku punktu mākoņa.
            </p>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 lg:py-12">
        <div className="grid gap-6 lg:grid-cols-[1fr_420px] lg:gap-8">
          <TreeVisualizer />
          <AnimationList
            animations={animations}
            selectedAnimation={selectedAnimation}
            onSelectAnimation={setSelectedAnimation}
          />
        </div>
      </main>
    </div>
  )
}
