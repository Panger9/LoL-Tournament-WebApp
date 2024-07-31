

//Nimmt ein array mit ranks als strings und ermittelt den durchschnittlichen rank
const RankMean = (rank) => {

  let result = ''

  if (!Array.isArray(rank)) {
    throw new Error('Parameter "rank" must be an array');
  }
  if (!rank.length < 1){
    const rankToPoints = [
      'IRON IV', 'IRON III', 'IRON II', 'IRON I',
      'BRONZE IV', 'BRONZE III', 'BRONZE II', 'BRONZE I',
      'SILVER IV', 'SILVER III', 'SILVER II', 'SILVER I',
      'GOLD IV', 'GOLD III', 'GOLD II', 'GOLD I',
      'PLATINUM IV', 'PLATINUM III', 'PLATINUM II', 'PLATINUM I',
      'EMERALD IV', 'EMERALD III', 'EMERALD II', 'EMERALD I',
      'DIAMOND IV', 'DIAMOND III', 'DIAMOND II', 'DIAMOND I',
      'MASTER', 'GRANDMASTER', 'CHALLENGER'
    ];
  
    let allPoints = 0
  
    for(let x = 0; x < rank.length; x++){
      for(let i = 0; i < rankToPoints.length; i++){
        if(rankToPoints[i] === rank[x]){
          allPoints = allPoints + i
        }
      }
    }
  
    const meanPoints = allPoints / rank.length;
    const roundedMeanPoints = Math.round(meanPoints);
    result = rankToPoints[roundedMeanPoints]
  }

  return result
}
 
export default RankMean;