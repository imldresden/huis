<script>
	import { Card, Button, Modal } from 'flowbite-svelte';
	// @ts-ignore
	import {  LinkSolid, CopySolid } from 'flowbite-svelte-icons';
	import { Tooltip } from 'flowbite-svelte';
	import { copyText } from 'svelte-copy';
	import PaperDetail from './paperDetail.svelte';
  import Multiselect from './multiselect.svelte';

	export let paper;
	export let structure;
	export let meta;
	export let index;
	let open = false;
</script>

<Tooltip trigger="click" triggeredBy={"#entry-"+index} placement="left">Copied Bibtex to clipboard!</Tooltip>

<Modal title="Paper Details" size='lg' id='modal' bind:open={open} outsideclose autoclose={false}>
	<PaperDetail {paper} detailView={structure.detailView} {meta} />
</Modal>

<Card 
	on:click={() => {open = true;}} 
	class="w-full m-1 dark:bg-[#212125] dark:shadow-xl"
	style="cursor: pointer;max-width: 95%;float:right"
	padding="none">
	<div class="grid grid-cols-7">
		<div class="ml-2 col-span-6" style="position:relative;">
			<span class="dark:text-white">{paper.Name} </span>
			<div class="text-gray-400" style="display:flex;padding-bottom:5px;padding-top:2px"><Multiselect list={[paper.source]}/> &nbsp; {paper.Year}</div>
		</div>
		<div class="">
			<Button on:click={
					(event) => {
						event.stopPropagation(); 
						window.open(paper.DOI.startsWith('10') ? 'https://doi.org/' + paper.DOI : paper.DOI);
					}
				} outline={true} size='xs' pill={true} class="!p-2 mb-2 mr-0.5 border-0 float-right">
				<LinkSolid class="w-4 h-4"/>
			</Button>
			{#if paper.Bibtex}
				<Button id={"entry-"+index}
						on:click={
						(event) => {
							event.stopPropagation(); 
							copyText(paper.Bibtex);
						} 
					} outline={true} size='xs' pill={true} class="!p-2 mb-2 mr-1 border-0 float-right">
					<CopySolid class="w-4 h-4" />
				</Button>
			{/if}
		</div>
	</div>
</Card>
