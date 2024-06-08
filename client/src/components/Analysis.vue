<template>
    <div class="container">
      <!--Durante la chiamata al server viene mostrato il caricamento-->
      <div v-if="loading" class="d-flex justify-content-center">
        <div class="spinner-border text-primary" role="status"></div>
      </div>
      <template v-else>
        <!--Input per inserire il testo da esaminare e button per inviare la richiesta al server-->
        <div class="input-group pb-3">
          <textarea v-model="testo" class="form-control" aria-label="With textarea"></textarea>
          <button @click="richiesta" type="button" class="btn btn-outline-primary">Cerca</button>
        </div>
        <!--Mostra il testo a video-->
        <div>
          {{ visualizza }}
        </div>
        <!--Alert in caso di errore della chiamata al server-->
        <div v-if="errore" class="alert alert-danger pb-3" role="alert">
          Errore nella chiamata al server(Dettagli in console)!
        </div>
        <template v-else-if="emozione === '1' || emozione === '0'">
          <p v-if="emozione === '0'"><b>Tristezza 😢</b></p>
          <p v-else> <b>Felicità 😄</b></p>
        </template>
      </template>
    </div>
  </template>
  
  <script>
  import axios from 'axios'; //Axios per chiamate al server
  
  export default {
    data() {
      return {
        testo: '', //Variabile per il testo inserito in input
        visualizza: '', //Variabile per mostrare il testo
        emozione: '', //Emozione restituita dal server basata sul testo
        loading: false, //Boolean per la gestione della chiamata al server
        errore: false, //Boolean che attiva l'alert in caso di errore nella chiamata al server
      };
    },
    methods: {
      //Funzione che definisce il payload per inviare la richiesta
      richiesta() {
        if(this.testo != ""){
          //Se l'utente ha inserito il testo si genera il payload
          this.presenza = false;
          const payload = {
            text: this.testo.toString()
          };
          //Viene eseguita la funzione per stabilire l'emozione
          this.findEmotion(payload);
          this.visualizza = this.testo;
          this.testo = "";
        }else{
          //Se l'utente non inserice del testo viene mostrato l'errore
          this.presenza = true;
        }
      },
      //Funzione che emette la chiamata al server per individuare l'emozione
      findEmotion(payload) {
        this.loading = true;
        const path = 'http://127.0.0.1:5002/esamina';
        //Tramite axios viene effettuata la richiesta passando payload e percorso
        axios.post(path, payload)
        .then((res) => {
          //Se la richiesta va a buon fine l'emozione individuata viene assegnata alla variabile corrispondente
          this.emozione = res.data.emotion;
          this.loading = false;
          this.errore = false;
        })  
        .catch((error) => {
          //Se la richiesta non va a buon fine viene mostrato l'alert di errore
          console.error(error);
          this.loading = false;
          this.errore = true;
        });
      },
    },
  };
  </script>