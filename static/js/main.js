const BASE_URL = '//scrap-visa-2021-hun7b.ondigitalocean.app';
// const BASE_URL = '//localhost:5000';

Vue.createApp({
    delimiters:["[[","]]"],
    data() {
        return {
            visaData:[],
            
        }
    },
    methods:{
        getTableData(){
            axios.get(`${BASE_URL}/api`).then(response =>{
                this.visaData = response.data;
                
            }).catch(error =>{
                console.log(error);
            
            })
        },
        getArrows(data, index){
            if(index < this.visaData.length - 1){
                if(parseInt(this.visaData[index][data]) > parseInt(this.visaData[index + 1][data])){
                        return true
                }
            }
           
        }
    },
    mounted(){
        this.getTableData();
     
    }
}).mount('#app')