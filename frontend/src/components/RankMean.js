

//Nimmt ein array mit ranks als strings und ermittelt den durchschnittlichen rank
const RankMean = (rank) => {

  let result = ''

  if (!Array.isArray(rank)) {
    throw new Error('Parameter "rank" must be an array');
  }
  if (!rank.length < 1){
    const rankToPoints = [
      'iron 4', 'iron 3', 'iron 2', 'iron 1',
      'bronze 4', 'bronze 3', 'bronze 2', 'bronze 1',
      'silver 4', 'silver 3', 'silver 2', 'silver 1',
      'gold 4', 'gold 3', 'gold 2', 'gold 1',
      'platinum 4', 'platinum 3', 'platinum 2', 'platinum 1',
      'emerald 4', 'emerald 3', 'emerald 2', 'emerald 1',
      'diamond 4', 'diamond 3', 'diamond 2', 'diamond 1',
      'master', 'grandmaster', 'challenger'
    ]
  
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