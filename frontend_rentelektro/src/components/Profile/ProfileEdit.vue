<template>
  <v-container class="profile-edit" max-width="600px">
    <v-card>
      <v-card-title>
        <h2>Edit Profile</h2>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="updateProfile">
          <v-row>
            <v-col cols="12">
              <v-text-field
                label="Zdjęcie profilowe"
                v-model="form.profile_picture"
                prepend-icon="mdi-camera"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                label="Nazwa użytkownika"
                v-model="form.username"
                prepend-icon="mdi-account"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                label="Imię"
                v-model="form.firstname"
                prepend-icon="mdi-account"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                label="Nazwisko"
                v-model="form.lastname"
                prepend-icon="mdi-account"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                label="Telefon"
                v-model="form.phone"
                prepend-icon="mdi-phone"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-checkbox
                label="Użytkownik biznesowy"
                v-model="form.company"
              ></v-checkbox>
            </v-col>
            <v-col cols="12">
              <v-text-field
                label="Email"
                v-model="form.email"
                prepend-icon="mdi-email"
                type="email"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-card-actions>
            <v-btn type="submit" color="primary">Zaktualizuj dane</v-btn>
          </v-card-actions>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'ProfileEdit',
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      form: {
        profile_picture: '',
        username: '',
        email: '',
        phone: '',
        firstname: '',
        lastname: '',
        company: false
      }
    };
  },
  watch: {
    user: {
      immediate: true,
      handler(newUser) {
        this.form = { ...newUser };
      }
    }
  },
  methods: {
    updateProfile() {
      this.$emit('update-profile', this.form);
    }
  }
}
</script>

<style scoped>
.profile-edit {
  padding: 20px;
}
</style>