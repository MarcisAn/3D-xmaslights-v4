<script lang="ts">
	import { onMount } from 'svelte';
	
	let snowflakes: any = $state([]);
	
	onMount(() => {
		// Create snowflakes
		const flakes = [];
		for (let i = 0; i < 20; i++) {
			flakes.push({
				id: i,
				left: Math.random() * 100,
				animationDuration: 10 + Math.random() * 20,
				animationDelay: Math.random() * 10,
				fontSize: 0.5 + Math.random() * 1
			});
		}
		snowflakes = flakes;
	});
</script>

{#each snowflakes as flake (flake.id)}
	<div 
		class="snowflake"
		style="
			left: {flake.left}%;
			animation-duration: {flake.animationDuration}s;
			animation-delay: {flake.animationDelay}s;
			font-size: {flake.fontSize}em;
		"
	>
		❄
	</div>
{/each}
