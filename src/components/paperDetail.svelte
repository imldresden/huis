<script>
	import { copyText } from 'svelte-copy';
	import Multiselect from './multiselect.svelte';
	import { Tooltip, Button, Heading, A } from 'flowbite-svelte';
	import { LinkSolid, CopySolid} from 'flowbite-svelte-icons';

	export let paper;
	export let detailView;
	export let meta;

</script>


<!-- {#if paper.image}
	<div style={"padding-right:10px"}>
			<img src={paper.image ? paper.image : "/images/defaultImage.png"} 
					width="200" height=200
					alt={paper.altImage ? paper.altImage: "Image from the paper"}
					/>
	</div>
{/if} -->
<div>
	<Heading tag="h4" style="margin: 0 20px 0 0 ;">
		{paper.Name} ({paper.Year})
	</Heading>
	<Heading tag="h6" style="margin: 0 0 10px; color: #888;">
		by {paper.Authors.join(", ")}
	</Heading>

	{#each detailView.show as prop}
		{#if meta[prop].type === 'String'}
			<div class="string-select">
				<div><strong>{prop}:&nbsp;</strong></div>
				<div>{paper[prop]}</div>
			</div>
		{:else if meta[prop].type === 'MultiSelect'}
			<div class="multi-select">
				<div><strong>{prop}:&nbsp</strong></div>
				{#if paper[prop].length > 0 && paper[prop][0] !== ''}
					<Multiselect list={paper[prop]} />
				{/if}
			</div>
		{/if}
	{/each}
	

	<br> 
	<div style="display:flex">
		{#if paper.source}
		<div class="string-select">
			<div><strong>Source:&nbsp;</strong></div>
			<Multiselect list={[paper.source]}/>
		</div>
		{/if}

		<div style="margin-left: auto;order: 2;">
			<Button on:click={
				(event) => {
					event.stopPropagation(); 
					window.open(paper.DOI.startsWith('10') ? 'https://doi.org/' + paper.DOI : paper.DOI);
				}
			} outline class="border-0">
				<LinkSolid class="w-4 h-4"/> &nbsp {paper.DOI} 
			</Button>
			
			<Button outline id="copyBibtex" class="border-0" on:click={(e)=>{copyText(paper.Bibtex);}}>
				<CopySolid class="w-4 h-4"/>
				<span>&nbsp Bibtex</span>
			</Button>
		
			<Tooltip trigger="click" triggeredBy="#copyBibtex" placement="right">Copied Bibtex</Tooltip>
		</div>
	</div>
</div>


<style>
	.multi-select {
		display: flex;
		align-items: center;
		justify-content: flex-start;
		flex-wrap: wrap;
		align-content: flex-start;
		padding: 2px 0px 2px 0px;
	}
	.string-select {
		height: 40px;
		display: flex;
		align-items: center;
		justify-content: flex-start;
		align-content: flex-start;
	}
</style>
