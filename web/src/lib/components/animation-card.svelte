<script>
	let { animation, isSelected, onselect } = $props();
</script>

<button onclick={() => onselect?.()} class="card-button">
	<div class="card" class:card-selected={isSelected}>
		{#if isSelected}
			<div class="selection-badge">
				<svg class="check-icon" fill="currentColor" viewBox="0 0 20 20">
					<path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
				</svg>
			</div>
		{/if}
		
		<div class="preview-container">
			<img 
				src={animation.preview || "/placeholder.svg"} 
				alt={animation.title}
				class="preview-image"
			/>
			
			<div class="preview-overlay"></div>
			
			<div class="corner-light corner-light-left twinkle"></div>
			<div class="corner-light corner-light-right twinkle" style="animation-delay: 0.5s;"></div>
		</div>
		
		<div class="card-content">
			<div class="card-header">
				<h3 class="card-title">
					{animation.title}
				</h3>
				<span class="card-emoji">🎄</span>
			</div>
			
			<p class="card-description">
				{animation.description}
			</p>
			
			<div class="card-footer">
				<div class="status-badge" class:status-selected={isSelected} class:status-unselected={!isSelected}>
					{isSelected ? '✓ Selected' : 'Tap to select'}
				</div>
			</div>
		</div>
	</div>
</button>

<style>
	.card-button {
		width: 100%;
		text-align: left;
		background: none;
		border: none;
		padding: 0;
		cursor: pointer;
		transition: transform 0.3s ease;
	}

	.card-button:hover {
		transform: scale(1.02);
	}

	.card-button:active {
		transform: scale(0.98);
	}

	.card {
		position: relative;
		border-radius: 0.75rem;
		overflow: hidden;
		border: 2px solid var(--border);
		background-color: var(--card);
		transition: all 0.3s ease;
	}

	.card-selected {
		border-color: var(--accent);
	}

	.selection-badge {
		position: absolute;
		top: 0.75rem;
		right: 0.75rem;
		z-index: 10;
		background-color: var(--accent);
		color: var(--accent-foreground);
		border-radius: 9999px;
		padding: 0.5rem;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	}

	.check-icon {
		width: 1.25rem;
		height: 1.25rem;
	}

	.preview-container {
		position: relative;
		aspect-ratio: 16/9;
		overflow: hidden;
		background-color: var(--muted);
	}

	.preview-image {
		width: 100%;
		height: 100%;
		object-fit: cover;
		transition: transform 0.3s ease;
	}

	.card-button:hover .preview-image {
		transform: scale(1.1);
	}

	.preview-overlay {
		position: absolute;
		inset: 0;
		background: linear-gradient(to top, rgba(20, 40, 25, 0.9), rgba(20, 40, 25, 0.2), transparent);
	}

	.corner-light {
		position: absolute;
		top: 0.5rem;
		width: 0.75rem;
		height: 0.75rem;
		border-radius: 9999px;
	}

	.corner-light-left {
		left: 0.5rem;
		background-color: var(--primary);
	}

	.corner-light-right {
		right: 0.5rem;
		background-color: var(--accent);
	}

	.card-content {
		padding: 1rem;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.card-header {
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: 0.5rem;
	}

	.card-title {
		font-size: 1.125rem;
		font-weight: bold;
		color: var(--foreground);
		line-height: 1.3;
	}

	.card-emoji {
		font-size: 1.5rem;
		flex-shrink: 0;
	}

	.card-description {
		font-size: 0.875rem;
		color: var(--muted-foreground);
		line-height: 1.6;
	}

	.card-footer {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding-top: 0.5rem;
	}

	.status-badge {
		padding: 0.25rem 0.75rem;
		border-radius: 9999px;
		font-size: 0.75rem;
		font-weight: bold;
		transition: all 0.3s ease;
	}

	.status-selected {
		background-color: var(--accent);
		color: var(--accent-foreground);
	}

	.status-unselected {
		background-color: var(--secondary);
		color: var(--secondary-foreground);
	}
</style>
