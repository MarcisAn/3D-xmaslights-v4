<script lang="ts">
  import "../app.css";
  import AnimationCard from "$lib/components/animation-card.svelte";
  import Snowfall from "$lib/components/snowfall.svelte";

  const animations = [
    {
      id: 1,
      title: "Classic Twinkle",
      description: "Traditional twinkling lights that sparkle randomly",
      preview: "/placeholder.svg?height=200&width=300",
    },
    {
      id: 2,
      title: "Rainbow Wave",
      description: "Colorful lights flowing in a wave pattern",
      preview: "/placeholder.svg?height=200&width=300",
    },
    {
      id: 3,
      title: "Candy Cane Chase",
      description: "Red and white lights chasing each other",
      preview: "/placeholder.svg?height=200&width=300",
    },
    {
      id: 4,
      title: "Snowfall Sparkle",
      description: "Lights cascading down like falling snow",
      preview: "/placeholder.svg?height=200&width=300",
    },
    {
      id: 5,
      title: "Golden Glow",
      description: "Warm golden lights pulsing gently",
      preview: "/placeholder.svg?height=200&width=300",
    },
    {
      id: 6,
      title: "Festive Fade",
      description: "Smooth color transitions through the spectrum",
      preview: "/placeholder.svg?height=200&width=300",
    },
  ];

  let selectedAnimation: any = $state(null);
</script>

<Snowfall />

<div class="container">
  <!-- Header with decorative elements -->
  <div class="header">
    <button
      onclick={() => {
        console.log("server", "aaa");
        let server_url = "";
          server_url = "http://localhost:3000";
        fetch(server_url + "/pickAnim", {
          method: "POST",
          body: JSON.stringify({name: "aaa"}),
          headers: new Headers({ "content-type": "application/json" }),
        });
      }}>fetch</button
    >
    <div class="header-stripe header-stripe-red"></div>
    <div class="header-stripe header-stripe-gold"></div>

    <h1 class="title twinkle">🎄 3D lampiņas 🎄</h1>
    <p class="subtitle">Izvēlies animāciju</p>
  </div>

  <!-- Live Christmas Tree Visualization -->
  <div class="tree-container">
    <div class="tree-frame glow">
      <div class="frame-stripe frame-stripe-top"></div>
      <div class="frame-stripe frame-stripe-bottom"></div>

      <iframe
        src="http://localhost:5173"
        title="Live Christmas Tree"
        class="tree-iframe"
        loading="lazy"
      ></iframe>

      <div class="live-badge">✨ VIZUALIZĀCIJA</div>
    </div>
  </div>

  <!-- Animation Selection Grid -->
  <div class="animations-section">
    <h2 class="section-title">
      <span class="emoji-left">🎅</span>
      <span>Animācijas</span>
      <span class="emoji-right">⭐</span>
    </h2>

    <div class="animations-grid">
      {#each animations as animation (animation.id)}
        <AnimationCard
          {animation}
          isSelected={selectedAnimation === animation.id}
          onselect={() => (selectedAnimation = animation.id)}
        />
      {/each}
    </div>
  </div>

  <!-- Footer decoration -->
  <div class="footer">
    <div class="footer-content">
      <span class="footer-emoji">❄️</span>
      <span>Merry Christmas!</span>
      <span class="footer-emoji-gold">🎁</span>
    </div>
  </div>
</div>

<style>
  .container {
    min-height: 100vh;
    padding-bottom: 2rem;
  }

  .header {
    position: relative;
    overflow: hidden;
    background: linear-gradient(
      to bottom,
      rgba(52, 130, 75, 0.2),
      var(--background)
    );
    padding-top: 1.5rem;
    padding-bottom: 1rem;
  }

  .header-stripe {
    position: absolute;
    left: 0;
    right: 0;
    height: 0.5rem;
  }

  .header-stripe-red {
    top: 0;
    background-color: var(--primary);
  }

  .header-stripe-gold {
    top: 0.5rem;
    background-color: var(--accent);
  }

  .title {
    text-align: center;
    font-size: 2.25rem;
    font-weight: bold;
    color: var(--accent);
    margin-bottom: 0.5rem;
    padding: 0 1rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  }

  .subtitle {
    text-align: center;
    color: var(--muted-foreground);
    font-size: 0.875rem;
    padding: 0 1rem;
  }

  .tree-container {
    padding: 1.5rem 1rem;
    margin: auto;
  }

  .tree-frame {
    position: relative;
    border-radius: 1rem;
    overflow: hidden;
    border: 4px solid var(--accent);
    background-color: var(--card);
    width: 300px;
    margin: auto;
  }

  .frame-stripe {
    position: absolute;
    left: 0;
    right: 0;
    height: 0.25rem;
    background-color: var(--primary);
    z-index: 1;
  }

  .frame-stripe-top {
    top: 0;
  }

  .frame-stripe-bottom {
    bottom: 0;
  }

  .tree-iframe {
    border: 0;
    display: block;
    width: 300px;
    height: 300px;
  }

  .live-badge {
    position: absolute;
    top: 0.5rem;
    left: 0.5rem;
    background-color: rgba(220, 38, 38, 0.9);
    color: var(--primary-foreground);
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: bold;
  }

  .animations-section {
    padding: 0 1rem;
  }

  .section-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--foreground);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .emoji-left {
    color: var(--primary);
  }

  .emoji-right {
    color: var(--accent);
  }

  .animations-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .footer {
    margin-top: 3rem;
    text-align: center;
    padding: 0 1rem;
  }

  .footer-content {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--muted-foreground);
    font-size: 0.875rem;
  }

  .footer-emoji {
    color: var(--primary);
  }

  .footer-emoji-gold {
    color: var(--accent);
  }

  @media (min-width: 640px) {
    .title {
      font-size: 3rem;
    }
  }
</style>
