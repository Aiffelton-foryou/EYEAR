import React, { useState } from "react";
import axios from "axios";
import ReactAudioPlayer from 'react-audio-player';
import { CameraFeed } from './components/camera-feed';

function Hang(){
    const [player,setPlayer] = useState();

    const imgHandler = async file =>{
        const formData = new FormData();
        formData.append('img',file);
        await axios.post("http://192.168.1.2:8000/app/imginf/",formData,{responseType:'blob'})
        .then(function(response){
            const sound = response.data;
            console.log(sound);
            // const blob = new Blob([sound], { type: 'audio/wav' });
            // console.log(blob);
            const url = (URL.createObjectURL(sound));
            
            setPlayer(<ReactAudioPlayer
                src={url}
                className="play_Audio"
                autoPlay
                controls
            />);
            
        }).catch(function (error){
            console.log(error);
        })
    }
    
    return (
    <>
        <section className="section">
			<h1 className="title">널위행</h1>
			<h2 className="subtitle">상품 알리미 서비스</h2>
		</section>
        
        <div>
            <div className="file-upload">
                <div className="image-upload-wrap">
                    <CameraFeed sendFile={imgHandler} />
                </div>
            </div>
            {player}
        </div>
    </>
    );
}
export default Hang;