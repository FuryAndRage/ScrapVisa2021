const BASE_URL = '//scrap-visa-2021-hun7b.ondigitalocean.app';
// const BASE_URL = '//localhost:5000';

Vue.createApp({
    delimiters:["[[","]]"],
    data() {
        return {
            visaData:[],
            visaDataFiltered:[],
            currentPage:1,
            totalPages:0,
            pageSize:10,
            currentPageRange:0,
            lastPageRange:0,
            loading:false,
        }
    },
    methods:{
        async getTableData(){
            await this.loadingPage(true)
            const response = await axios.get(`${BASE_URL}/api`)
            this.visaData = response.data;
            this.visaDataFiltered = this.visaData
            this.currentPageRange = 0
            // console.log(this.visaData[0])
            this.lastPageRange = this.visaData.length
            this.visaDataFiltered.splice(this.lastPageRange, this.currentPageRange);
            this.totalPages = Math.ceil(this.visaData.length / this.pageSize);

            await this.loadingPage(false)
            // await axios.get(`${BASE_URL}/api`).then(response =>{
            //     this.visaData = response.data;
            //     this.visaDataFiltered = this.visaData
            //     this.currentPageRange = 0
            //     // console.log(this.visaData[0])
            //     this.lastPageRange = this.visaData.length
            //     this.visaDataFiltered.splice(this.lastPageRange, this.currentPageRange);
            //     this.totalPages = Math.ceil(this.visaData.length / this.pageSize);
                
            // }).catch(error =>{
            //     console.log(error);
            // })
        },
        async loadingPage(status){
            this.loading = status
            if(this.loading){
                SlickLoader.enable();
            }
            else{
                SlickLoader.disable();
            }
        },
        movePageUp(){
            console.log(this.visaData)
            this.visaDataFiltered = this.visaData
            this.currentPage += 1
            this.currentPageRange -= 10
            this.lastPageRange -=  10
            this.visaDataFiltered.splice(this.lastPageRange, this.currentPageRange)
            console.log(this.currentPageRange)
        },
        movePageDown(){
            this.visaDataFiltered = this.visaData
            this.currentPage -= 1
            this.currentPageRange += 10
            this.lastPageRange += 10
            this.visaDataFiltered.splice(this.lastPageRange, this.currentPageRange)
            console.log(this.currentPageRange)
        },
        getArrows(data, index){
            if(index < this.visaData.length - 1){
                if(parseInt(this.visaData[index][data]) > parseInt(this.visaData[index + 1][data])){
                    return true
                }
            }
        }
    },
    computed:{
        orderByPagination(){
            return this.visaData.sort((a,b) => {
                return parseInt(a.pagination) - parseInt(b.pagination)
            })
        }
    },
    mounted(){
        this.getTableData();
        
     
    },
    beforeMount(){
        window.addEventListener("beforeunload", function (event) {
            // event.returnValue = "\o/";
            SlickLoader.enable();
          });
    }
    
}).mount('#app')