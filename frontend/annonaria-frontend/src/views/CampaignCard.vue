<!-- Represents an individual campaign in a card layout. -->
<!-- Displays campaign details and emits actions (edit, delete, toggle) to the parent component. -->

<template>
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{{ campaign.name }}</h5>

        <!-- Campaign description (scrollable if long) -->
        <p class="card-text-scroll">{{ campaign.description }}</p>

        <!-- Start and end dates -->
        <p class="card-text">
          <strong>Start:</strong> {{ campaign.start_date }} <br />
          <strong>End:</strong> {{ campaign.end_date }}
        </p>
        
         <!-- Budget -->
        <p class="card-text"><strong>Budget:</strong> ${{ campaign.budget }}</p>
  
        <!-- Status badge: Active or Inactive -->
        <p class="card-text">
          <span class="badge" :class="campaign.is_active ? 'badge-active' : 'badge-inactive'">
            {{ campaign.is_active ? 'Active' : 'Inactive' }}
          </span>
        </p>
  
       <!-- Action buttons: Edit, Delete, Toggle status -->
        <button class="btn btn-sm btn-primary me-1" @click="editCampaign(campaign.id)">Edit</button>
        <button class="btn btn-sm btn-danger me-1" @click="deleteCampaign(campaign.id)">Delete</button>
        <button class="btn btn-sm btn-secondary" @click="toggleCampaign(campaign.id)">
          {{ campaign.is_active ? 'Deactivate' : 'Activate' }}
        </button>
      </div>
    </div>
  </template>
  
  <script>
  import '../assets/campaignCard.css';
  
  export default {
    name: 'CampaignCard',
    props: {
      campaign: Object
    },
    methods: {
      // Emit events to the parent with the campaign ID
      editCampaign(id) {
        this.$emit('edit', id); 
      },
      deleteCampaign(id) {
        this.$emit('delete', id); 
      },
      toggleCampaign(id) {
        this.$emit('toggle', id); 
      }
    }
  };
  </script>
  