<template>
  <v-container>
    <v-form @submit.prevent="addTool" ref="form" v-model="isValid">
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            label="Type"
            v-model="tool.Type"
            :rules="[v => !!v || 'Type is required']"
            required
            outlined
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            label="Power Source"
            v-model="tool.PowerSource"
            :items="powerSources"
            :rules="[v => !!v || 'Power Source is required']"
            required
            outlined
          ></v-select>
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            label="Brand"
            v-model="tool.Brand"
            :rules="[v => !!v || 'Brand is required']"
            required
            outlined
          ></v-text-field>
        </v-col>
        <v-col cols="12">
          <v-text-field
            label="Description"
            v-model="tool.Description"
            :rules="[v => !!v || 'Description is required']"
            required
            outlined
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
              label="Category ID"
              v-model="tool.CategoryID"
              :rules="[v => !!v || 'Category ID is required']"
              required
              type="number"
              outlined
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-checkbox
              label="Availability"
              v-model="tool.Availability"
              outlined
          ></v-checkbox>
        </v-col>
        <v-col cols="12" md="6">
          <v-checkbox
              label="Insurance"
              v-model="tool.Insurance"
              outlined
          ></v-checkbox>
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
              label="Power"
              v-model="tool.Power"
              :rules="[v => !!v || 'Power is required']"
              required
              type="number"
              outlined
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
              label="Age"
              v-model="tool.Age"
              :rules="[v => !!v || 'Age is required']"
              required
              type="number"
              step="0.1"
              outlined
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
              label="Rate Per Day"
              v-model="tool.RatePerDay"
              :rules="[v => !!v || 'Rate Per Day is required']"
              required
              type="number"
              step="0.01"
              outlined
          ></v-text-field>
        </v-col>
        <v-col cols="12">
          <v-text-field
              label="Image URL"
              v-model="tool.ImageURL"
              :rules="[v => !!v || 'Image URL is required']"
              required
              outlined
          ></v-text-field>
        </v-col>
        <v-col cols="12">
          <v-btn color="primary" type="submit">Add Tool</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ToolAddForm',
  data() {
    return {
      tool: {
        Type: '',
        PowerSource: '',
        Brand: '',
        Description: '',
        CategoryID: null,
        Availability: false,
        Insurance: false,
        Power: null,
        Age: null,
        RatePerDay: null,
        ImageURL: '',
      },
      powerSources: ['electric', 'gas'], // or fetch these dynamically
      isValid: false,
    };
  },
  methods: {
    async addTool() {
      if (!this.$refs.form.validate()) {
        return;
      }
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.post('api/tool/add', this.tool, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        });
        this.$refs.form.reset();  // Reset the form after successful submission
        this.$emit('tool-added');  // Emit an event to inform the parent component
      } catch (error) {
        alert(`Failed to add tool: ${error.response.data.detail}`);
      }
    },
  },
};
</script>

<style scoped>
.v-text-field,
.v-checkbox,
.v-btn {
  margin-bottom: 20px;
}
</style>