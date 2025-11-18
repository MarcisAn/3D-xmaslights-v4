'use client'

import { Card } from '@/components/ui/card'
import { Animation } from '@/app/page'
import { Check } from 'lucide-react'
import { cn } from '@/lib/utils'

interface AnimationListProps {
  animations: Animation[]
  selectedAnimation: Animation
  onSelectAnimation: (animation: Animation) => void
}

export function AnimationList({
  animations,
  selectedAnimation,
  onSelectAnimation,
}: AnimationListProps) {
  return (
    <Card className="flex flex-col border-0 bg-card/95 backdrop-blur-md shadow-2xl">
      <div className="bg-primary/30 px-6 py-4 border-b-[6px] border-primary">
        <h2 className="font-bold text-xl text-foreground">Animation Styles</h2>
        <p className="text-sm text-foreground/90">
          Choose your festive light pattern
        </p>
      </div>
      <div className="flex-1 space-y-3 p-6">
        {animations.map((animation) => {
          const isSelected = selectedAnimation.id === animation.id
          return (
            <button
              key={animation.id}
              onClick={() => onSelectAnimation(animation)}
              className={cn(
                'group relative w-full border-l-[6px] bg-muted/80 p-4 text-left transition-all hover:bg-secondary/30 hover:border-secondary hover:shadow-lg',
                isSelected
                  ? 'border-primary bg-primary/20 shadow-xl'
                  : 'border-transparent'
              )}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1">
                  <h3 className="font-bold text-foreground">
                    {animation.name}
                  </h3>
                  <p className="mt-1 text-sm text-foreground/80">
                    {animation.description}
                  </p>
                </div>
                <div className="flex h-6 w-6 shrink-0 items-center justify-center bg-primary text-primary-foreground opacity-0 transition-opacity data-[selected=true]:opacity-100 shadow-lg" data-selected={isSelected}>
                  <Check className="h-4 w-4" />
                </div>
              </div>
            </button>
          )
        })}
      </div>
    </Card>
  )
}
